from pydantic import BaseModel

from .models import Location as LocationDatabaseModel


class Location(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float

    class Config:
        db_model = LocationDatabaseModel
