from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.accounts.domain import Account
from src.accounts.services import AccountServices
from src.auth.services import get_current_active_user
from src.core.pagination import Paginator
from src.core.schemas import PaginationSchema, PaginationRequestSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.unit_of_work import DeviceEnergyUnitOfWork
from src.device_types.domain import DeviceType
from src.device_types.unit_of_work import DeviceTypeUnitOfWork
from src.devices.domain import Device
from src.devices.unit_of_work import DeviceUnitOfWork
from src.location_weather.domain import LocationWeather
from src.location_weather.unit_of_work import LocationWeatherUnitOfWork
from src.locations.domain import Location
from src.locations.unit_of_work import LocationUnitOfWork
from src.projects.domain import Project
from src.projects.unit_of_work import ProjectUnitOfWork
from src.reports.domain import Report
from src.reports.exceptions import ReportDoesNotExistsException
from src.reports.schemas import ReportCreateUpdateSchema
from src.reports.services import ReportServices
from src.reports.unit_of_work import ReportUnitOfWork

report_router = fastapi.routing.APIRouter(
    prefix='/reports'
)


@report_router.post("", response_model=Report, tags=['Reports'])
async def create_report(
        form_data: ReportCreateUpdateSchema,
        report_uow: Annotated[
            AbstractUnitOfWork[Report],
            Depends(ReportUnitOfWork)
        ],
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
        device_energies_uow: Annotated[
            AbstractUnitOfWork[DeviceEnergy],
            Depends(DeviceEnergyUnitOfWork)
        ],
        device_type_uow: Annotated[
            AbstractUnitOfWork[DeviceType],
            Depends(DeviceTypeUnitOfWork)
        ],
        location_weather_uow: Annotated[
            AbstractUnitOfWork[LocationWeather],
            Depends(LocationWeatherUnitOfWork)
        ],
        project_uow: Annotated[
            AbstractUnitOfWork[Project],
            Depends(ProjectUnitOfWork)
        ],
        current_user: Annotated[Account, Depends(get_current_active_user)]
):
    report = await ReportServices.generate_report(
        date_from=form_data.date_from,
        date_to=form_data.date_to,
        project_id=form_data.project_id,
        report_uow=report_uow,
        location_uow=location_uow,
        location_weather_uow=location_weather_uow,
        device_uow=device_uow,
        device_type_uow=device_type_uow,
        device_energies_uow=device_energies_uow,
        project_uow=project_uow
    )
    report_template = await ReportServices.generate_report_template(
        report=report,
        project_uow=project_uow,
        project_id=form_data.project_id
    )
    await AccountServices.send_email_to_user(
        account=current_user,
        subject='Report for project',
        body=report_template
    )
    return report



@report_router.get("", response_model=PaginationSchema[Report], tags=['Reports'])
async def get_reports_list(
        report_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ReportUnitOfWork)
        ],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    devices = await report_uow.list(**pagination.dict())
    count = await report_uow.count()
    paginator = Paginator[Report](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@report_router.get("/{id}", response_model=Report, tags=['Reports'])
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


@report_router.put("/{id}", response_model=Report, tags=['Reports'])
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


@report_router.delete("/{id}", tags=['Reports'])
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
