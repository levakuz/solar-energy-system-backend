from typing import Optional

from pydantic import BaseModel


class DeviceCreateUpdateSchema(BaseModel):
    device_type_id: int
    project_id: int
    location_id: int
    power_peak: float
    orientation: float
    count: int


class DeviceFilterSchema(BaseModel):
    device_type_id: Optional[int]
    project_id: Optional[int]
    location_id: Optional[int]
