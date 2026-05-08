from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from core.database import Base

class DBConnection(Base):
    __tablename__ = "db_connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    engine = Column(String(50), nullable=False)
    host = Column(String(500), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(200), nullable=True)
    encrypted_password = Column(Text, nullable=True)
    database_name = Column(String(200), nullable=True)
    extra_params = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
