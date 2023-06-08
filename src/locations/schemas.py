from pydantic import BaseModel


class LocationCreateUpdateSchema(BaseModel):
    name: str
    longitude: float
    latitude: float
