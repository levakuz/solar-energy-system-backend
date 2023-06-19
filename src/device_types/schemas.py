from typing import Optional

from pydantic import BaseModel


class DeviceTypeCreateSchema(BaseModel):
    company_id: int
    name: str
    area: str
    system_loss: str


class DeviceTypeFilterSchema(BaseModel):
    company_id: Optional[int]
