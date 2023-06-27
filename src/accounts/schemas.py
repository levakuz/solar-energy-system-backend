from pydantic import BaseModel

from src.accounts.models import AccountStatus, UserAccountType


class CompanyRegistrationSchema(BaseModel):
    email: str
    password: str
    name: str


class UserRegistrationSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserAccountSchema(BaseModel):
    first_name: str
    last_name: str


class AccountSchema(BaseModel):
    email: str
    phone_number: str | None
    status: AccountStatus


class AccountDeleteSchema(BaseModel):
    status: AccountStatus = AccountStatus.inactive


class CompanyAccountSchema(BaseModel):
    account_id: int
    name: str


class UserAccountTypeSchema(BaseModel):
    type: UserAccountType
