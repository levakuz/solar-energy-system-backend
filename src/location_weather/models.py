from datetime import datetime
from typing import Optional

from beanie import Document, Indexed


class LocationWeather(Document):
    location_id: Indexed(int)
    date: datetime
    direct_normal_irradiance: Optional[float]
    cloudcover: Optional[float]

    class Settings:
        name = "location_weather"
