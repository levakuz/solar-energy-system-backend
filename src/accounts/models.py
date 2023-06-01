import enum

from tortoise import Model
from tortoise.fields import CharField, CharEnumField, ForeignKeyField, OneToOneField, CASCADE

from src.core.models import BaseModel


class AccountStatus(enum.StrEnum):
    active = 'active'
    inactive = 'inactive'


class Account(BaseModel):
    email = CharField(max_length=255, unique=True, null=False)
    phone_number = CharField(max_length=255, unique=True, null=True)
    status = CharEnumField(enum_type=AccountStatus, default=AccountStatus.active)
    password = CharField(max_length=255, null=False)

    class Meta:
        table = "Account"


class CompanyAccount(Model):
    account = OneToOneField('models.Account', related_name='company_account', on_delete=CASCADE, pk=True)
    name = CharField(max_length=255, unique=True)

    class Meta:
        table = "CompanyAccount"


class UserAccountType(enum.StrEnum):
    free = 'free'
    unlimited = 'unlimited'


class UserAccount(Model):
    account = OneToOneField('models.Account', related_name='user_account', on_delete=CASCADE, pk=True)
    type = CharEnumField(enum_type=UserAccountType, default=UserAccountType.free)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)

    class Meta:
        table = "UserAccount"
