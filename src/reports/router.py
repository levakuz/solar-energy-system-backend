from typing import Annotated, List

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.core.unit_of_work import AbstractUnitOfWork
from src.reports.domain import Report
from src.reports.exceptions import ReportDoesNotExistsException
from src.reports.schemas import ReportCreateUpdateSchema
from src.reports.unit_of_work import ReportUnitOfWork

report_router = fastapi.routing.APIRouter(
    prefix='/reports'
)


@report_router.post("/", response_model=Report, tags=['Reports'])
async def create_report(
        form_data: ReportCreateUpdateSchema,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.add(**form_data.dict())


@report_router.get("/", response_model=List[Report], tags=['Reports'])
async def get_reports_list(
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    return await report_uow.list()


@report_router.get("/{id}/", response_model=Report, tags=['Reports'])
async def get_report(
        id: int,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    try:
        return await report_uow.get(id=id)
    except ReportDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@report_router.put("/{id}/", response_model=Report, tags=['Reports'])
async def update_report(
        id: int,
        form_data: ReportCreateUpdateSchema,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    try:
        return await report_uow.update(id=id, update_object=form_data)
    except ReportDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@report_router.delete("/{id}/", tags=['Reports'])
async def delete_report(
        id: int,
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
):
    try:
        return await report_uow.delete(id=id)
    except ReportDoesNotExistsException as e:
        return
