from pydantic import BaseModel

from src.device_types import DeviceType as DeviceTypeDatabaseModel


class DeviceType(BaseModel):
    id: int
    name: str
    area: str
    system_loss: str

    class Config:
        db_model = DeviceTypeDatabaseModel
