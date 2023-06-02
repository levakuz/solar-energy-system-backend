from typing import Annotated, NoReturn

from asyncpg import UniqueViolationError
from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.accounts.domain import UserAccount, Account, CompanyAccount
from src.accounts.exceptions import AccountDoesNotExistsException, AccountWithEmailAlreadyExistsException, \
    CompanyWithNameAlreadyExistsException
from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork


class AccountUnitOfWork(AbstractUnitOfWork[Account]):
    def __init__(
            self,
            account_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=Account,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._account_repository = account_repository

    async def get(self, *args, **kwargs) -> Account:
        try:
            return await self._account_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def add(self, *args, **kwargs) -> Account:
        try:
            return await self._account_repository.add(*args, **kwargs)
        except IntegrityError as e:
            if type(e.args[0]) is UniqueViolationError:
                if e.args[0].constraint_name == 'Account_email_key':
                    raise AccountWithEmailAlreadyExistsException
                else:
                    raise e
            else:
                raise e

    async def update(self, update_object: BaseModel, **kwargs) -> Account:
        try:
            return await self._account_repository.update(update_object=update_object, **kwargs)
        except IntegrityError as e:
            if type(e.args[0]) is UniqueViolationError:
                if e.args[0].constraint_name == 'Account_email_key':
                    raise AccountWithEmailAlreadyExistsException
                else:
                    raise e
        except DoesNotExist:
            raise AccountDoesNotExistsException

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._account_repository.delete(*args, **kwargs)


class UserAccountUnitOfWork(AbstractUnitOfWork[UserAccount]):
    def __init__(
            self,
            user_account_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=UserAccount,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._account_repository = user_account_repository

    async def get(self, *args, **kwargs) -> UserAccount:
        try:
            return await self._account_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> UserAccount:
        try:
            await self._account_repository.update(update_object=update_object, **kwargs)
            return await self._account_repository.get(**kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def add(self, *args, **kwargs) -> UserAccount:
        return await self._account_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._account_repository.delete(*args, **kwargs)


class CompanyAccountUnitOfWork(AbstractUnitOfWork[CompanyAccount]):
    def __init__(
            self,
            company_account_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=CompanyAccount,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._account_repository = company_account_repository

    async def get(self, *args, **kwargs) -> CompanyAccount:
        try:
            return await self._account_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> CompanyAccount:
        try:
            await self._account_repository.update(update_object=update_object, **kwargs)
            return await self._account_repository.get(**kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException
        except IntegrityError as e:
            if type(e.args[0]) is UniqueViolationError:
                if e.args[0].constraint_name == 'CompanyAccount_name_key':
                    raise CompanyWithNameAlreadyExistsException
                else:
                    raise e
            else:
                raise e

    async def add(self, *args, **kwargs) -> CompanyAccount:
        try:
            return await self._account_repository.add(*args, **kwargs)
        except IntegrityError as e:
            if type(e.args[0]) is UniqueViolationError:
                if e.args[0].constraint_name == 'CompanyAccount_name_key':
                    raise CompanyWithNameAlreadyExistsException
                else:
                    raise e
            else:
                raise e

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._account_repository.delete(*args, **kwargs)
