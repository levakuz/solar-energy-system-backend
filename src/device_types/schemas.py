from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel


class DeviceTypeCreateSchema(BaseModel):
    company_id: int
    name: str
    area: float
    system_loss: float
    efficiency: float
    photo: UploadFile

    @classmethod
    def as_form(
            cls,
            company_id: int = Form(...),
            name: str = Form(...),
            area: float = Form(...),
            system_loss: float = Form(...),
            efficiency: float = Form(...),
            photo: UploadFile = Form(...),
    ) -> BaseModel:
        return cls(
            name=name,
            company_id=company_id,
            area=area,
            system_loss=system_loss,
            efficiency=efficiency,
            photo=photo
        )


class DeviceTypeFilterSchema(BaseModel):
    company_id: Optional[int]
