import datetime

from pydantic import BaseModel

from src.projects.models import Project as ProjectDatabaseModel
from src.projects.models import AccountStatus

class Project(BaseModel):
    id: int
    account_id: int
    name: str
    created_at: datetime
    status: AccountStatus

    class Config:
        db_model = ProjectDatabaseModel
