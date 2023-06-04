from tortoise.fields import CharField, ForeignKeyField
from src.core.models import BaseModel


class DeviceType(BaseModel):
    company = ForeignKeyField('models.CompanyAccount', related_name='company_devices', to_field='account_id')
    name = CharField(max_length=255, unique=True, null=False)
    area = CharField(max_length=255, null=True)
    system_loss = CharField(max_length=255, null=False)

    class Meta:
        table = "device_type"

    def __repr__(self):
        return f'DeviceType {self.id}'

    def __str__(self):
        return f'DeviceType {self.id}'
