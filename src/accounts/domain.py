from pydantic import BaseModel

from src.accounts.models import AccountStatus
from src.accounts.models import Account as AccountDatabaseModel


class Account(BaseModel):

    email: str
    phone_number: str | None
    status: AccountStatus
    password: str

    class Config:
        db_model = AccountDatabaseModel
