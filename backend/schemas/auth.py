from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", v):
            raise ValueError("Username solo puede tener letras, números y _ (3-30 chars)")
        return v

    @field_validator("password")
    @classmethod
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    username: str
    role: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str]
    oauth_provider: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

class SessionOut(BaseModel):
    id: UUID
    ip_address: Optional[str]
    login_method: str
    created_at: datetime
    expires_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}

class ActivityLogOut(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    detail: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

class OAuthUserData(BaseModel):
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    provider: str
    provider_id: str
