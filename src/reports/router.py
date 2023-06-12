from typing import Annotated

import fastapi
from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.reports.domain import Report
from src.reports.schemas import ReportCreateUpdateSchema
from src.reports.unit_of_work import ReportUnitOfWork

report_router = fastapi.routing.APIRouter(
    prefix='/reports'
)


@report_router.post("", response_model=Report, tags=['Reports'])
async def create_report(
        form_data: ReportCreateUpdateSchema,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.add(**form_data.dict())


@report_router.get("/{id}", response_model=Report, tags=['Reports'])
async def get_report(
        id: int,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.get(id=id)


@report_router.put("/{id}", response_model=Report, tags=['Reports'])
async def update_report(
        id: int,
        form_data: ReportCreateUpdateSchema,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.update(id=id, update_object=form_data)


@report_router.delete("/{id}", tags=['Reports'])
async def delete_report(
        id: int,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.delete(id=id)
