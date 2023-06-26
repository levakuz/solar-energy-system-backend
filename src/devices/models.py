from tortoise.fields import CharField, ForeignKeyField, FloatField, TextField
from src.core.models import BaseModel


class Device(BaseModel):
    device_type = ForeignKeyField('models.DeviceType',related_name='d.type_devices', to_field='')
    project = ForeignKeyField('models.Project',related_name='project_devices')
    location = ForeignKeyField('models.Location',related_name='location_devices')
    name = TextField(max_length=255, null=False)
    orientation = FloatField(null=True)
    tilt = FloatField(null=True)
    count = CharField(max_length=255, null=True)
    class Meta:
        table = "device"

    def __repr__(self):
        return f'Device {self.id}'

    def __str__(self):
        return f'Device {self.id}'
