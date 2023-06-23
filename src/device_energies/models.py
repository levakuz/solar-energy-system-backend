from tortoise.fields import FloatField, ForeignKeyField, DatetimeField

from src.core.models import BaseModel


class DeviceEnergy(BaseModel):
    device = ForeignKeyField('models.Device', related_name='device_d.energies')
    date = DatetimeField()
    value = FloatField(null=True)

    class Meta:
        table = "device_energy"
        unique_together = (("device", "date"),)

    def __repr__(self):
        return f'DeviceEnergy {self.id}'

    def __str__(self):
        return f'DeviceEnergy {self.id}'
