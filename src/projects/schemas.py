from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.projects.models import ProjectStatus


class ProjectCreateUpdateSchema(BaseModel):
    name: str
    account_id: int


class ProjectFilterSchema(BaseModel):
    account_id: Optional[int]
    status: Optional[ProjectStatus]
