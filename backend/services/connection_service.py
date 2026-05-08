from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.connection import DBConnection
from schemas.connection import ConnectionCreate, ConnectionOut, ConnectionTest, SchemaAnalysis
from connectors.factory import get_connector
from core.encryption import encrypt_password, decrypt_password
from fastapi import HTTPException
from datetime import datetime, timezone
from uuid import UUID

async def save_connection(db: AsyncSession, user_id: UUID, data: ConnectionCreate, password: str = None) -> DBConnection:
    encrypted = encrypt_password(password) if password else None
    conn = DBConnection(
        user_id=user_id,
        name=data.name,
        engine=data.engine.value,
        host=data.host,
        port=data.port,
        username=data.username,
        encrypted_password=encrypted,
        database_name=data.database_name,
        extra_params=data.extra_params,
    )
    db.add(conn)
    await db.flush()
    return conn

async def get_user_connections(db: AsyncSession, user_id: UUID) -> list[DBConnection]:
    result = await db.execute(
        select(DBConnection).where(DBConnection.user_id == user_id, DBConnection.is_active == True)
        .order_by(DBConnection.created_at.desc())
    )
    return result.scalars().all()

async def get_connection_by_id(db: AsyncSession, conn_id: UUID, user_id: UUID) -> DBConnection:
    result = await db.execute(
        select(DBConnection).where(DBConnection.id == conn_id, DBConnection.user_id == user_id)
    )
    conn = result.scalar_one_or_none()
    if not conn:
        raise HTTPException(status_code=404, detail="Conexión no encontrada")
    return conn

async def test_connection_service(data: ConnectionCreate, password: str = None) -> ConnectionTest:
    connector = get_connector(data, password)
    return await connector.test_connection()

async def analyze_connection_service(db: AsyncSession, conn_id: UUID, user_id: UUID) -> SchemaAnalysis:
    db_conn = await get_connection_by_id(db, conn_id, user_id)
    from schemas.connection import DBEngine
    config = ConnectionCreate(
        name=db_conn.name,
        engine=DBEngine(db_conn.engine),
        host=db_conn.host,
        port=db_conn.port,
        username=db_conn.username,
        database_name=db_conn.database_name,
        extra_params=db_conn.extra_params,
    )
    password = decrypt_password(db_conn.encrypted_password) if db_conn.encrypted_password else None
    connector = get_connector(config, password)
    schema = await connector.analyze_schema()
    await db.execute(update(DBConnection).where(DBConnection.id == conn_id).values(last_used_at=datetime.now(timezone.utc)))
    return schema

async def delete_connection(db: AsyncSession, conn_id: UUID, user_id: UUID):
    await get_connection_by_id(db, conn_id, user_id)
    await db.execute(update(DBConnection).where(DBConnection.id == conn_id).values(is_active=False))
