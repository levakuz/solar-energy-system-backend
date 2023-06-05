from typing import Optional

from pydantic import BaseModel

from src.accounts.models import Account as AccountDatabaseModel, UserAccountType, AccountRole
from src.accounts.models import AccountStatus
from src.accounts.models import CompanyAccount as CompanyAccountDatabaseModel
from src.accounts.models import UserAccount as UserAccountDatabaseModel


class Account(BaseModel):
    id: int
    email: str
    phone_number: str | None
    status: AccountStatus
    password: str
    role: AccountRole

    class Config:
        db_model = AccountDatabaseModel


class CompanyAccount(BaseModel):
    account_id: int
    name: str
    account: Optional[Account]

    class Config:
        db_model = CompanyAccountDatabaseModel


class UserAccount(BaseModel):
    account_id: int
    first_name: str | None
    last_name: str | None
    type: UserAccountType | None

    class Config:
        db_model = UserAccountDatabaseModel
