from datetime import datetime
from src.projects.models import ProjectStatus
from pydantic import BaseModel


class ProjectCreateUpdateSchema(BaseModel):
    name: str
    account_id: int
    created_at: datetime
    status: ProjectStatus
