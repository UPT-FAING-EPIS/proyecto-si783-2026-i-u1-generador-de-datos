from cryptography.fernet import Fernet
from core.config import settings
import base64, hashlib

def _get_fernet() -> Fernet:
    key = hashlib.sha256(settings.secret_key.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_password(password: str) -> str:
    if not password:
        return ""
    return _get_fernet().encrypt(password.encode()).decode()

def decrypt_password(encrypted: str) -> str:
    if not encrypted:
        return ""
    return _get_fernet().decrypt(encrypted.encode()).decode()
