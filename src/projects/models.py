import datetime
import enum

from tortoise.fields import CharField, ForeignKeyField, DatetimeField, CharEnumField

from src.core.models import BaseModel


class ProjectStatus(enum.StrEnum):
    active = 'active'
    inactive = 'inactive'


class Project(BaseModel):
    account = ForeignKeyField('models.UserAccount', related_name='user_projects', to_field='account_id')
    name = CharField(max_length=255, null=False)
    created_at = DatetimeField(default=datetime.datetime.now)
    status = CharEnumField(enum_type=ProjectStatus, default=ProjectStatus.active)

    class Meta:
        table = "project"

    def __repr__(self):
        return f'Project {self.id}'

    def __str__(self):
        return f'Project {self.id}'