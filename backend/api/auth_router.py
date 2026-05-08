from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from core.database import get_db
from schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut, UserUpdate, ChangePassword, OAuthUserData, SessionOut, ActivityLogOut
from services.auth_service import register_user, login_user, oauth_login_or_register
from auth.dependencies import get_current_user, require_admin
from models.user import User, Session, ActivityLog
from core.security import hash_password, verify_password
from typing import List
import httpx

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=TokenResponse, summary="Registrar nuevo usuario")
async def register(data: UserRegister, request: Request, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, data, request)
    from core.security import create_access_token
    token, _ = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role.value,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
    )

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
async def login(data: UserLogin, request: Request, db: AsyncSession = Depends(get_db)):
    user, token = await login_user(db, data.email, data.password, request)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role.value,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
    )

@router.get("/me", response_model=UserOut, summary="Obtener usuario actual")
async def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut, summary="Actualizar perfil")
async def update_me(data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if update_data:
        await db.execute(update(User).where(User.id == current_user.id).values(**update_data))
    result = await db.execute(select(User).where(User.id == current_user.id))
    return result.scalar_one()

@router.post("/change-password", summary="Cambiar contraseña")
async def change_password(data: ChangePassword, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.hashed_password:
        raise HTTPException(status_code=400, detail="Esta cuenta usa OAuth, no tiene contraseña")
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    await db.execute(update(User).where(User.id == current_user.id).values(hashed_password=hash_password(data.new_password)))
    return {"message": "Contraseña actualizada correctamente"}

@router.post("/logout", summary="Cerrar sesión")
async def logout(request: Request, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    from fastapi.security import HTTPBearer
    from core.security import decode_token
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "")
    payload = decode_token(token)
    if payload:
        jti = payload.get("jti")
        await db.execute(update(Session).where(Session.token_jti == jti).values(is_active=False))
    return {"message": "Sesión cerrada correctamente"}

@router.get("/sessions", response_model=List[SessionOut], summary="Mis sesiones activas")
async def my_sessions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Session).where(Session.user_id == current_user.id, Session.is_active == True).order_by(Session.created_at.desc())
    )
    return result.scalars().all()

@router.post("/oauth/google", response_model=TokenResponse, summary="Login con Google")
async def oauth_google(token: dict, request: Request, db: AsyncSession = Depends(get_db)):
    access_token = token.get("access_token")
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token de Google inválido")
    info = resp.json()
    data = OAuthUserData(email=info["email"], full_name=info.get("name"), avatar_url=info.get("picture"), provider="google", provider_id=info["id"])
    user, jwt_token = await oauth_login_or_register(db, data, request)
    return TokenResponse(access_token=jwt_token, user_id=str(user.id), email=user.email, username=user.username, role=user.role.value, full_name=user.full_name, avatar_url=user.avatar_url)

@router.post("/oauth/github", response_model=TokenResponse, summary="Login con GitHub")
async def oauth_github(token: dict, request: Request, db: AsyncSession = Depends(get_db)):
    access_token = token.get("access_token")
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.github.com/user", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"})
        email_resp = await client.get("https://api.github.com/user/emails", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"})
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token de GitHub inválido")
    info = resp.json()
    emails = email_resp.json() if email_resp.status_code == 200 else []
    primary_email = next((e["email"] for e in emails if e.get("primary")), info.get("email"))
    if not primary_email:
        raise HTTPException(status_code=400, detail="No se pudo obtener email de GitHub")
    data = OAuthUserData(email=primary_email, full_name=info.get("name"), avatar_url=info.get("avatar_url"), provider="github", provider_id=str(info["id"]))
    user, jwt_token = await oauth_login_or_register(db, data, request)
    return TokenResponse(access_token=jwt_token, user_id=str(user.id), email=user.email, username=user.username, role=user.role.value, full_name=user.full_name, avatar_url=user.avatar_url)
