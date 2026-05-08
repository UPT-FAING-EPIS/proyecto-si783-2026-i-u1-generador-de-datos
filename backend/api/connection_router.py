from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Any, Dict
from core.database import get_db
from auth.dependencies import get_current_user
from models.user import User
from schemas.connection import ConnectionCreate, ConnectionOut, ConnectionTest, SchemaAnalysis, DBEngine
from services.connection_service import (
    save_connection, get_user_connections, test_connection_service,
    analyze_connection_service, delete_connection,
)
from typing import List
from uuid import UUID

router = APIRouter(prefix="/connections", tags=["Conexiones"])

class ConnectionWithPassword(BaseModel):
    name: str
    engine: DBEngine
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database_name: Optional[str] = None
    extra_params: Optional[Dict[str, Any]] = None

@router.post("/test", response_model=ConnectionTest, summary="Probar conexion sin guardar")
async def test_conn(
    body: ConnectionWithPassword,
    current_user: User = Depends(get_current_user),
):
    data = ConnectionCreate(
        name=body.name,
        engine=body.engine,
        host=body.host,
        port=body.port,
        username=body.username,
        database_name=body.database_name,
        extra_params=body.extra_params,
    )
    return await test_connection_service(data, body.password)

@router.post("/", response_model=ConnectionOut, summary="Guardar conexion")
async def create_conn(
    body: ConnectionWithPassword,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = ConnectionCreate(
        name=body.name,
        engine=body.engine,
        host=body.host,
        port=body.port,
        username=body.username,
        database_name=body.database_name,
        extra_params=body.extra_params,
    )
    conn = await save_connection(db, current_user.id, data, body.password)
    return conn

@router.get("/", response_model=List[ConnectionOut], summary="Listar mis conexiones")
async def list_conns(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_user_connections(db, current_user.id)

@router.get("/{conn_id}/analyze", response_model=SchemaAnalysis, summary="Analizar esquema de BD")
async def analyze(
    conn_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await analyze_connection_service(db, conn_id, current_user.id)

@router.delete("/{conn_id}", summary="Eliminar conexion")
async def delete_conn(
    conn_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_connection(db, conn_id, current_user.id)
    return {"message": "Conexion eliminada"}
