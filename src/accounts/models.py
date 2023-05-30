import enum

from tortoise.fields import CharField, CharEnumField

from src.core.models import BaseModel


class AccountStatus(enum.StrEnum):
    active = 'active'
    inactive = 'inactive'


class Account(BaseModel):
    email = CharField(max_length=255, unique=True, null=False)
    phone_number = CharField(max_length=255, unique=True, null=True)
    status = CharEnumField(enum_type=AccountStatus, default=AccountStatus.active)
    password = CharField(max_length=255, null=False)
