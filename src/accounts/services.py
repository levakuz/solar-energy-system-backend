from fastapi_mail import MessageSchema, FastMail
from pydantic import BaseModel
from tortoise.transactions import atomic

from src.accounts.domain import Account
from src.accounts.models import AccountRole
from src.accounts.schemas import AccountDeleteSchema
from src.auth.services import get_password_hash
from src.core.unit_of_work import AbstractUnitOfWork
from src.settings import settings


@atomic()
async def register_account(
        email: str,
        password: str,
        role: AccountRole,
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
    account = await account_uow.add(
        email=email,
        password=hashed_password,
        role=role
    )
    user_account = await child_account_uow.add(
        account_id=account.id,
        **kwargs
    )
    return account


@atomic()
async def mark_account_as_inactive(
        account_uow: AbstractUnitOfWork[Account],
        id: int
):
    account = await account_uow.update(id=id, update_object=AccountDeleteSchema())
    return account


async def send_email_to_user(
        account: Account,
        subject: str,
        body: str,
):
    message = MessageSchema(
        subject=subject,
        recipients=[account.email],
        body=body,
        subtype='html'
    )
    fm = FastMail(settings.MAIL_SETTINGS)
    await fm.send_message(message)
