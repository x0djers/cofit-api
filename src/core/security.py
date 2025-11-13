from datetime import datetime, timedelta, UTC

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            days=settings.SECURE.TOKEN_LIFETIME_DAYS
        )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECURE.SECRET_KEY.get_secret_value(),
        algorithm=settings.SECURE.HASH_ALGORITHM
    )

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token,
                          settings.SECURE.SECRET_KEY.get_secret_value(),
                          algorithms=[settings.SECURE.HASH_ALGORITHM])
    except JWTError:
        return {}