from pydantic import BaseModel
from datetime import datetime

from src.device_energies.models import DeviceEnergy as DeviceEnergyDatabaseModel


class DeviceEnergy(BaseModel):
    id: int
    device_id: int
    date: datetime
    value: float


    class Config:
        db_model = DeviceEnergyDatabaseModel
