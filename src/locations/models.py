from tortoise.fields import CharField, FloatField

from src.core.models import BaseModel


class Location(BaseModel):
    name = CharField(max_length=255, unique=True, null=True)
    longitude = FloatField(null=False)
    latitude = FloatField(null=False)

    class Meta:
        table = "location"

    def __repr__(self):
        return f'Location {self.id}'

    def __str__(self):
        return f'Location {self.id}'
