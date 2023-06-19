from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceEnergyCreateSchema(BaseModel):
    device_id: int
    date: datetime
    value: float


class DeviceEnergyFilterSchema(BaseModel):
    device_id: Optional[int]
