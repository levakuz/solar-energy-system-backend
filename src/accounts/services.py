from fastapi_mail import MessageSchema, FastMail
from pydantic import BaseModel
from tortoise.transactions import atomic

from src.accounts.domain import Account
from src.accounts.models import AccountRole
from src.accounts.schemas import AccountDeleteSchema
from src.auth.services import get_password_hash
from src.core.unit_of_work import AbstractUnitOfWork
from src.settings import settings


class AccountServices:

    @atomic()
    @classmethod
    async def register_account(
            cls,
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
    @classmethod
    async def mark_account_as_inactive(
            cls,
            account_uow: AbstractUnitOfWork[Account],
            id: int
    ):
        account = await account_uow.update(id=id, update_object=AccountDeleteSchema())
        return account

    @classmethod
    async def send_email_to_user(
            cls,
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
