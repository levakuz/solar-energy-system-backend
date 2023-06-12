from tortoise.fields import CharField, ForeignKeyField
from src.core.models import BaseModel


class Device(BaseModel):
    device_type = ForeignKeyField('models.DeviceType',related_name='d.type_devices', to_field='')
    project = ForeignKeyField('models.Project',related_name='project_devices')
    location = ForeignKeyField('models.Location',related_name='location_devices')
    power_peak = CharField(max_length=255, null=True)
    orientation = CharField(max_length=255, null=True)
    count = CharField(max_length=255, null=True)
    class Meta:
        table = "device"

    def __repr__(self):
        return f'Device {self.id}'

    def __str__(self):
        return f'Device {self.id}'
