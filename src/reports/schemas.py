from datetime import datetime

from pydantic import BaseModel


class ReportCreateUpdateSchema(BaseModel):
    project_id: int
    date_from: datetime
    date_to: datetime


class ReportGenerateSchema(BaseModel):
    project_id: int
    date_from: datetime
    date_to: datetime
    value: float
    plot_path: str


class ReportFilterSchema(BaseModel):
    project_id: int
