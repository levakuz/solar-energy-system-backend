from src.accounts.domain import UserAccount
from src.auth.services import get_password_hash
from src.core.repository import AbstractRepository


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
    account = await account_repository.add(email=email, password=hashed_password, commit=False)
    user_account = await child_account_repository.add(
        account_id=account.id,
        **kwargs
    )
    return account
