from tortoise.fields import ForeignKeyField, DatetimeField, FloatField, TextField

from src.core.models import BaseModel


class Report(BaseModel):
    project = ForeignKeyField('models.Project', related_name='project_reports')
    date_from = DatetimeField()
    date_to = DatetimeField()
    value = FloatField(null=False)
    plot_path = TextField()

    class Meta:
        table = "report"

    def __repr__(self):
        return f'Report {self.id}'

    def __str__(self):
        return f'Report {self.id}'
