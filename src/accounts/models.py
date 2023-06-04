import enum

from tortoise import Model, OneToOneFieldInstance
from tortoise.fields import CharField, CharEnumField, OneToOneField, CASCADE, ForeignKeyField

from src.core.models import BaseModel


class AccountRole(enum.StrEnum):
    COMPANY = 'company'
    USER = 'user'


class AccountStatus(enum.StrEnum):
    active = 'active'
    inactive = 'inactive'


class Account(BaseModel):
    email = CharField(max_length=255, unique=True, null=False)
    phone_number = CharField(max_length=255, unique=True, null=True)
    status = CharEnumField(enum_type=AccountStatus, default=AccountStatus.active)
    password = CharField(max_length=255, null=False)
    role = CharEnumField(enum_type=AccountRole, null=False)

    class Meta:
        table = "account"

    def __repr__(self):
        return f'Account {self.id}'

    def __str__(self):
        return f'Account {self.id}'


class CompanyAccount(Model):
    account = OneToOneField(
        'models.Account',
        related_name='company_account',
        on_delete=CASCADE,
        pk=True
    )  # type: OneToOneFieldInstance[Account]
    name = CharField(max_length=255, unique=True)

    class Meta:
        table = "company_account"


class UserAccountType(enum.StrEnum):
    free = 'free'
    unlimited = 'unlimited'


class UserAccount(Model):
    account = OneToOneField(
        'models.Account',
        related_name='user_account',
        on_delete=CASCADE,
        pk=True
    )  # type: OneToOneFieldInstance[Account]
    type = CharEnumField(enum_type=UserAccountType, default=UserAccountType.free)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)

    class Meta:
        table = "user_account"



