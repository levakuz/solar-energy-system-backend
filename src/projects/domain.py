from datetime import datetime

from pydantic import BaseModel

from src.projects.models import Project as ProjectDatabaseModel
from src.projects.models import ProjectStatus

class Project(BaseModel):
    id: int
    account_id: int
    name: str
    created_at: datetime
    status: ProjectStatus

    class Config:
        db_model = ProjectDatabaseModel
