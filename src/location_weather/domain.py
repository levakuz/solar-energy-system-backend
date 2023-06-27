from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.location_weather.models import LocationWeather as LocationWeatherDatabaseModel


class LocationWeather(BaseModel):
    location_id: int
    date: datetime
    direct_normal_irradiance: float
    cloudcover: float

    class Config:
        db_model = LocationWeatherDatabaseModel
