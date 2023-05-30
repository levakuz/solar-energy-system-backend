from pydantic import BaseModel

from src.accounts.models import AccountStatus


class Account(BaseModel):
    email: str
    phone_number: str | None
    status: AccountStatus
    password: str
