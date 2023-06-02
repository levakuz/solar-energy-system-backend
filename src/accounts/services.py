from asyncpg import UniqueViolationError
from tortoise.exceptions import IntegrityError, DoesNotExist
from tortoise.transactions import atomic

from src.accounts.domain import UserAccount
from src.accounts.exceptions import AccountWithEmailAlreadyExistsException, CompanyWithNameAlreadyExistsException, \
    UserDoesNotExistsException
from src.accounts.schemas import AccountDeleteSchema
from src.auth.services import get_password_hash
from src.core.repository import AbstractRepository


@atomic()
async def register_account(
        email: str,
        password: str,
        account_repository: AbstractRepository,
        child_account_repository: AbstractRepository,
        **kwargs
) -> UserAccount:
    """
    Register user in service with provided email and password
    :param email: email
    :param password: plain password
    :param account_repository: Account repository
    :return: Account domain model
    """
    hashed_password = get_password_hash(password)
    try:
        account = await account_repository.add(email=email, password=hashed_password)
        user_account = await child_account_repository.add(
            account_id=account.id,
            **kwargs
        )
        return account
    except IntegrityError as e:
        if type(e.args[0]) is UniqueViolationError:
            if e.args[0].constraint_name == 'Account_email_key':
                raise AccountWithEmailAlreadyExistsException
            elif e.args[0].constraint_name == 'CompanyAccount_name_key':
                raise CompanyWithNameAlreadyExistsException
            else:
                raise e


@atomic()
async def delete_account(
        account_repository: AbstractRepository,
        id: int
):
    try:
        account = await account_repository.update(id=id, update_object=AccountDeleteSchema())
        return account
    except DoesNotExist as e:
        raise UserDoesNotExistsException
