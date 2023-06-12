from pydantic import BaseModel

from src.devices.models import Device as DeviceDatabaseModel


class Device(BaseModel):
    id: int
    device_type_id: int
    project_id: int
    location_id: int
    power_peak: float
    orientation: float
    count: int


    class Config:
        db_model = DeviceDatabaseModel
