from pydantic import BaseModel


class DeviceTypeCreateSchema(BaseModel):
    name: str
    area: str
    system_loss: str
