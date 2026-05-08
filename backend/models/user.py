from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from core.database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(200), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(500), nullable=True)
    oauth_provider = Column(String(50), nullable=True)
    oauth_id = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    token_jti = Column(String(200), unique=True, nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    login_method = Column(String(50), default="email")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    action = Column(String(200), nullable=False)
    detail = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
