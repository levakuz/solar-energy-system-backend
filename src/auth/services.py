from typing import Type, Annotated

import tortoise
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from src.accounts.domain import Account
from src.accounts.models import AccountStatus
from src.accounts.repository import AccountRepository
from src.auth.exceptions import credentials_exception
from src.auth.schemas import TokenData
from src.auth.utils import crypto_context, oauth2_scheme
from src.core.repository import AbstractRepository
from src.settings import Settings


def verify_password(
        plain_password: str,
        hashed_password: str,
        pwd_context=crypto_context
):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str, pwd_context=crypto_context):
    return pwd_context.hash(password)


async def authenticate_user(
        repository: Type[AbstractRepository],
        email: str,
        password: str,
):
    try:
        user = await repository.get(email=email)
    except tortoise.exceptions.DoesNotExist:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await AccountRepository().get(email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[Account, Depends(get_current_user)]
):
    if current_user.status == AccountStatus.inactive:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def register_user(email: str, password: str):
    hashed_password = get_password_hash(password)
    return await AccountRepository().add(email=email, password=hashed_password)
