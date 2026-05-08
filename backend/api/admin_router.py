from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, desc
from core.database import get_db
from auth.dependencies import require_admin
from models.user import User, Session, ActivityLog
from schemas.auth import UserOut, SessionOut, ActivityLogOut
from typing import List

router = APIRouter(prefix="/admin", tags=["Administración"])

@router.get("/users", response_model=List[UserOut], summary="Listar todos los usuarios")
async def list_users(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()

@router.get("/users/active-sessions", summary="Usuarios con sesiones activas")
async def active_sessions(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(
        select(Session, User).join(User, Session.user_id == User.id)
        .where(Session.is_active == True)
        .order_by(desc(Session.created_at))
    )
    rows = result.all()
    return [
        {
            "session_id": str(s.id),
            "user_id": str(u.id),
            "email": u.email,
            "username": u.username,
            "role": u.role.value,
            "ip_address": s.ip_address,
            "login_method": s.login_method,
            "created_at": s.created_at,
            "expires_at": s.expires_at,
        }
        for s, u in rows
    ]

@router.post("/users/{user_id}/block", summary="Bloquear usuario")
async def block_user(user_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    await db.execute(update(User).where(User.id == user_id).values(is_active=False))
    await db.execute(update(Session).where(Session.user_id == user_id).values(is_active=False))
    return {"message": "Usuario bloqueado y sesiones revocadas"}

@router.post("/users/{user_id}/unblock", summary="Desbloquear usuario")
async def unblock_user(user_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    await db.execute(update(User).where(User.id == user_id).values(is_active=True))
    return {"message": "Usuario desbloqueado"}

@router.delete("/sessions/{session_id}", summary="Revocar sesión específica")
async def revoke_session(session_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    await db.execute(update(Session).where(Session.id == session_id).values(is_active=False))
    return {"message": "Sesión revocada"}

@router.get("/logs", response_model=List[ActivityLogOut], summary="Historial de actividad")
async def activity_logs(limit: int = 100, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(
        select(ActivityLog).order_by(desc(ActivityLog.created_at)).limit(limit)
    )
    return result.scalars().all()

@router.get("/stats", summary="Estadísticas del sistema")
async def stats(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    total_users = await db.scalar(select(func.count(User.id)))
    active_users = await db.scalar(select(func.count(User.id)).where(User.is_active == True))
    active_sessions = await db.scalar(select(func.count(Session.id)).where(Session.is_active == True))
    total_logs = await db.scalar(select(func.count(ActivityLog.id)))
    logins_by_method = await db.execute(
        select(Session.login_method, func.count(Session.id)).group_by(Session.login_method)
    )
    return {
        "total_users": total_users,
        "active_users": active_users,
        "blocked_users": total_users - active_users,
        "active_sessions": active_sessions,
        "total_activity_logs": total_logs,
        "logins_by_method": {row[0]: row[1] for row in logins_by_method.all()},
    }
