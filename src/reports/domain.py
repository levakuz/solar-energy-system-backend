from datetime import datetime

from pydantic import BaseModel

from .models import Report as ReportDatabaseModel


class Report(BaseModel):
    id: int
    project_id: int
    date_from: datetime
    date_to: datetime
    value: float
    plot_path: str

    class Config:
        db_model = ReportDatabaseModel
