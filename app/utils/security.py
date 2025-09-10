from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets, hashlib
from app.core.config import settings

# HASHing
passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)


def create_access_token(user_data , expires_delta: timedelta = None):
    now = datetime.now()
    expire = now + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = secrets.token_urlsafe(64)
    payload = {"sub": str(user_data.id), 
               "email": user_data.email, 
               "role": user_data.role, 
               "token_version": user_data.token_version, 
               "iat": now,
               "jti": jti,
               "exp": expire
               }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return token


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_refresh_token(raw_refresh_token: str) -> str:
    return hashlib.sha256(raw_refresh_token.encode()).hexdigest()

def verify_refresh_token(raw_refresh_token: str, stored_hashed_refresh_token: str) -> bool:
    return hash_refresh_token(raw_refresh_token) == stored_hashed_refresh_token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            [settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise e
