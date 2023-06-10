from datetime import datetime
from src.projects.models import AccountStatus
from pydantic import BaseModel


class ProjectCreateUpdateSchema(BaseModel):
    name: str
    created_at: datetime
    status: AccountStatus
