from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationWeather(BaseModel):
    location_id: int
    date: datetime
    direct_normal_irradiance: Optional[float]
    cloudcover: Optional[float]
