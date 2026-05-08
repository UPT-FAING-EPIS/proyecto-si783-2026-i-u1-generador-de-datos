from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.user import User, Session, ActivityLog
from schemas.auth import UserRegister, OAuthUserData
from core.security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Request
import uuid

async def log_activity(db: AsyncSession, user_id, action: str, detail: str = None, request: Request = None):
    ip = None
    ua = None
    if request:
        ip = request.client.host if request.client else None
        ua = request.headers.get("user-agent")
    log = ActivityLog(
        user_id=user_id,
        action=action,
        detail=detail,
        ip_address=ip,
        user_agent=ua,
    )
    db.add(log)
    await db.flush()

async def register_user(db: AsyncSession, data: UserRegister, request: Request = None):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    result2 = await db.execute(select(User).where(User.username == data.username))
    if result2.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El username ya está en uso")

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    await db.flush()
    await log_activity(db, user.id, "REGISTER", "Registro con email/password", request)
    return user

async def login_user(db: AsyncSession, email: str, password: str, request: Request = None):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    token, jti = create_access_token({"sub": str(user.id), "role": user.role.value})

    ip = request.client.host if request and request.client else None
    ua = request.headers.get("user-agent") if request else None

    session = Session(
        user_id=user.id,
        token_jti=jti,
        ip_address=ip,
        user_agent=ua,
        login_method="email",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=60),
    )
    db.add(session)
    await log_activity(db, user.id, "LOGIN", "Login con email/password", request)
    return user, token

async def oauth_login_or_register(db: AsyncSession, data: OAuthUserData, request: Request = None):
    result = await db.execute(
        select(User).where(User.oauth_provider == data.provider, User.oauth_id == data.provider_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        result2 = await db.execute(select(User).where(User.email == data.email))
        user = result2.scalar_one_or_none()

    if user:
        await db.execute(
            update(User).where(User.id == user.id).values(
                oauth_provider=data.provider,
                oauth_id=data.provider_id,
                avatar_url=data.avatar_url or user.avatar_url,
            )
        )
    else:
        base_username = data.email.split("@")[0].replace(".", "_")[:20]
        username = base_username
        i = 1
        while True:
            r = await db.execute(select(User).where(User.username == username))
            if not r.scalar_one_or_none():
                break
            username = f"{base_username}_{i}"
            i += 1

        user = User(
            email=data.email,
            username=username,
            full_name=data.full_name,
            avatar_url=data.avatar_url,
            oauth_provider=data.provider,
            oauth_id=data.provider_id,
            is_verified=True,
        )
        db.add(user)
        await db.flush()

    token, jti = create_access_token({"sub": str(user.id), "role": user.role.value})

    ip = request.client.host if request and request.client else None
    ua = request.headers.get("user-agent") if request else None
    session = Session(
        user_id=user.id,
        token_jti=jti,
        ip_address=ip,
        user_agent=ua,
        login_method=data.provider,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=60),
    )
    db.add(session)
    await log_activity(db, user.id, "LOGIN_OAUTH", f"Login con {data.provider}", request)
    return user, token

async def get_current_user_by_token(db: AsyncSession, payload: dict):
    user_id = payload.get("sub")
    jti = payload.get("jti")
    if not user_id or not jti:
        raise HTTPException(status_code=401, detail="Token inválido")

    result = await db.execute(
        select(Session).where(Session.token_jti == jti, Session.is_active == True)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Sesión expirada o revocada")

    result2 = await db.execute(select(User).where(User.id == user_id))
    user = result2.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    return user
