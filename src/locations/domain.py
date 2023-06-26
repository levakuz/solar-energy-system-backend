from typing import Optional

from pydantic import BaseModel

from .models import Location as LocationDatabaseModel


class Location(BaseModel):
    id: int
    name: Optional[str]
    longitude: float
    latitude: float

    class Config:
        db_model = LocationDatabaseModel

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id

    def __hash__(self):
        return hash((self.name, self.id))
