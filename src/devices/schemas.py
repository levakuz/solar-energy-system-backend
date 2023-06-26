from typing import Optional, List

from pydantic import BaseModel


class DeviceCreateUpdateSchema(BaseModel):
    name: str
    device_type_id: int
    project_id: int
    location_id: int
    tilt: float
    orientation: float
    count: int


class DeviceFilterSchema(BaseModel):
    device_type_id: Optional[int]
    project_id: Optional[int]
    location_id: Optional[int]
