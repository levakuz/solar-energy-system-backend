from typing import List, Optional

from pydantic import BaseModel


class LocationCreateUpdateSchema(BaseModel):
    name: Optional[str]
    longitude: float
    latitude: float


class LocationGeocodingResponseSchema(BaseModel):
    longitude: float
    latitude: float


class LocationGeocodingAPIResultSchema(BaseModel):
    longitude: float
    latitude: float
    name: str
    country_code: str


class LocationGeocodingAPIResponseSchema(BaseModel):
    results: Optional[List[LocationGeocodingAPIResultSchema]]
