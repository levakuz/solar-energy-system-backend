from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.accounts.domain import Account, UserAccount
from src.accounts.unit_of_work import UserAccountUnitOfWork
from src.auth.services import get_current_active_user
from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
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
from src.projects.exceptions import ProjectDoesNotExistsException, ProjectLimitForAccountExceededException
from src.projects.schemas import ProjectCreateUpdateSchema, ProjectFilterSchema
from src.projects.services import ProjectServices
from src.projects.unit_of_work import ProjectUnitOfWork
from src.reports.domain import Report
from src.reports.unit_of_work import ReportUnitOfWork

project_router = fastapi.routing.APIRouter(
    prefix='/projects'
)


@project_router.post("", response_model=Project, tags=['Projects'])
async def create_project(
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
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
        user_account_uow: Annotated[
            AbstractUnitOfWork[UserAccount],
            Depends(UserAccountUnitOfWork)
        ],
        current_user: Annotated[Account, Depends(get_current_active_user)],
        form_data: ProjectCreateUpdateSchema = Depends(ProjectCreateUpdateSchema.as_form),
):
    try:
        project = await ProjectServices.try_to_create_project(
            project_uow=project_uow,
            user_account_uow=user_account_uow,
            project=form_data,
            current_user=current_user
        )
        await ProjectServices.schedule_report_creation_for_30_days(
            report_uow=report_uow,
            project=project,
            current_user=current_user,
            location_uow=location_uow,
            location_weather_uow=location_weather_uow,
            device_uow=device_uow,
            device_type_uow=device_type_uow,
            device_energies_uow=device_energies_uow,
            project_uow=project_uow
        )
    except ProjectLimitForAccountExceededException as e:
        return JSONResponse(status_code=400, content={'detail': e.message})
    return project


@project_router.get("", response_model=PaginationSchema[Project], tags=['Projects'])
async def get_projects_list(
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
        filters: Annotated[ProjectFilterSchema, Depends(ProjectFilterSchema)],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    devices = await project_uow.list(**filters.dict(), **pagination.dict())
    count = await project_uow.count(**filters.dict())
    paginator = Paginator[Project](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@project_router.get("/{id}", response_model=Project, tags=['Projects'])
async def get_project(
        id: int,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.get(id=id)
    except ProjectDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@project_router.put("/{id}", response_model=Project, tags=['Projects'])
async def update_project(
        id: int,
        form_data: ProjectCreateUpdateSchema,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.update(id=id, update_object=form_data)
    except ProjectDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@project_router.delete("/{id}", tags=['Projects'])
async def delete_project(
        id: int,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.delete(id=id)
    except ProjectDoesNotExistsException as e:
        return
