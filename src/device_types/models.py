from tortoise.fields import CharField, ForeignKeyField, TextField, FloatField

from src.core.models import BaseModel


class DeviceType(BaseModel):
    company = ForeignKeyField('models.CompanyAccount', related_name='company_devices', to_field='account_id')
    name = CharField(max_length=255, unique=True, null=False)
    area = FloatField(null=False)
    efficiency = FloatField(null=False)
    system_loss = FloatField(null=False)
    photo = TextField()

    class Meta:
        table = "device_type"

    def __repr__(self):
        return f'DeviceType {self.id}'

    def __str__(self):
        return f'DeviceType {self.id}'
