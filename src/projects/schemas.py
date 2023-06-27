from typing import Optional

from fastapi import UploadFile, Form
from pydantic import BaseModel

from src.projects.models import ProjectStatus


class ProjectCreateUpdateSchema(BaseModel):
    name: str
    account_id: int
    photo: UploadFile

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            account_id: int = Form(...),
            photo: UploadFile = Form(...),
    ) -> BaseModel:
        return cls(name=name, account_id=account_id, photo=photo)


class ProjectFilterSchema(BaseModel):
    account_id: Optional[int]
    status: Optional[ProjectStatus]


class ProjectUpdateStatusSchema(BaseModel):
    status: ProjectStatus
