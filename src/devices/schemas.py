from pydantic import BaseModel


class DeviceCreateUpdateSchema(BaseModel):
    device_type_id: int
    project_id: int
    location_id: int
    power_peak: float
    orientation: float
    count: int
    

