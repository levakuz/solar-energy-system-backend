from pydantic import BaseModel
from datetime import datetime


class DeviceEnergyCreateSchema(BaseModel):
    device_id: int
    date: datetime
    value: float

