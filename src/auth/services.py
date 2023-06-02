from typing import Annotated

import tortoise
from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.accounts.domain import Account
from src.accounts.exceptions import AccountDoesNotExistsException, InactiveUserException
from src.accounts.models import AccountStatus
from src.auth.exceptions import InvalidCredentialsException
from src.auth.schemas import TokenData
from src.auth.utils import crypto_context, oauth2_scheme
from src.core.repository import AbstractRepository, TortoiseRepository
from src.core.repository_factory import RepositoryFactory
from src.settings import Settings, settings


def verify_password(
        plain_password: str,
        hashed_password: str,
        pwd_context: CryptContext = crypto_context
) -> bool:
    """
    Verify provided plain password with hash password
    :param plain_password: Plain string password
    :param hashed_password: Hashed password
    :param pwd_context: CryptContext object
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(
        password: str,
        pwd_context: CryptContext = crypto_context
) -> str:
    """
    Get hash from plain string password
    :param password: plain password
    :param pwd_context: CryptContext object
    :return: Hashed password
    """
    return pwd_context.hash(password)


async def authenticate_user(
        repository: AbstractRepository,
        email: str,
        password: str,
) -> Account:
    """
    Returns if credentials passed validation
    :param repository: Account repository
    :param email: string with email
    :param password: plain password
    :return: Account domain model
    """
    try:
        user = await repository.get(email=email)
    except tortoise.exceptions.DoesNotExist:
        raise AccountDoesNotExistsException
    if not verify_password(password, user.password):
        raise InvalidCredentialsException
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=Account,
                type_repository=TortoiseRepository
            ))
        ]
) -> Account:
    """
    Get user by JWT.
    :param token: JWT
    :param account_repository: Account repository
    :return: Account domain model
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username: str | None = payload.get("sub")  # Type: str
        if username is None:
            raise InvalidCredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise InvalidCredentialsException
    user = await account_repository.get(email=token_data.username)  # type: Account
    if user is None:
        raise InvalidCredentialsException
    return user


async def get_current_active_user(
        current_user: Annotated[Account, Depends(get_current_user)]
):
    """
    Validate that user is active
    :param current_user: Account domain object that need to be checked
    :return: Account domain model
    """
    if current_user.status == AccountStatus.inactive:
        raise InactiveUserException
    return current_user
