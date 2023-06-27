from pydantic import BaseModel

from src.device_types.models import DeviceType as DeviceTypeDatabaseModel


class DeviceType(BaseModel):
    id: int
    company_id: int
    name: str
    area: float
    system_loss: float
    efficiency: float
    photo: str

    class Config:
        db_model = DeviceTypeDatabaseModel
