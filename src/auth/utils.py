from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from src.auth.auth_bearer import JWTBearer
from src.settings import Settings, settings

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = JWTBearer()


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

