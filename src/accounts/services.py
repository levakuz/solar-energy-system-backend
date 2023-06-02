from pydantic import BaseModel
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from src.accounts.exceptions import AccountDoesNotExistsException
from src.accounts.schemas import AccountDeleteSchema
from src.auth.services import get_password_hash
from src.core.unit_of_work import AbstractUnitOfWork


@atomic()
async def register_account(
        email: str,
        password: str,
        account_uow: AbstractUnitOfWork,
        child_account_uow: AbstractUnitOfWork,
        **kwargs
) -> BaseModel:
    """
    Register user in service with provided email and password
    :param email: email
    :param password: plain password
    :param account_repository: Account repository
    :return: Account domain model
    """
    hashed_password = get_password_hash(password)
    account = await account_uow.add(email=email, password=hashed_password)
    user_account = await child_account_uow.add(
        account_id=account.id,
        **kwargs
    )
    return account


@atomic()
async def mark_account_as_inactive(
        account_uow: AbstractUnitOfWork,
        id: int
):
    account = await account_uow.update(id=id, update_object=AccountDeleteSchema())
    return account

