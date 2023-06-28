from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.auth.services import get_current_active_user
from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_types.domain import DeviceType
from src.device_types.exceptions import DeviceTypeDoesNotExistsException
from src.device_types.schemas import DeviceTypeCreateSchema, DeviceTypeFilterSchema
from src.device_types.unit_of_work import DeviceTypeUnitOfWork

device_type_router = fastapi.routing.APIRouter(
    prefix='/device-types',
    dependencies=[Depends(get_current_active_user)],
)


@device_type_router.post("", response_model=DeviceType, tags=['Device Types'])
async def create_device_type(
        device_type_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
        form_data: DeviceTypeCreateSchema = Depends(DeviceTypeCreateSchema.as_form),
):
    return await device_type_uow.add(**form_data.dict())


@device_type_router.get("", response_model=PaginationSchema[DeviceType], tags=['Device Types'])
async def device_types_list(
        device_type_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
        filters: Annotated[DeviceTypeFilterSchema, Depends(DeviceTypeFilterSchema)],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)]
):
    devices = await device_type_uow.list(**filters.dict(), **pagination.dict())
    count = await device_type_uow.count(**filters.dict())
    paginator = Paginator[DeviceType](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@device_type_router.get("/{id}", response_model=DeviceType, tags=['Device Types'])
async def get_device_type(
        id: int,
        device_type_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await device_type_uow.get(id=id)
    except DeviceTypeDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_type_router.put("/{id}", response_model=DeviceType, tags=['Device Types'])
async def update_device_type(
        id: int,
        form_data: DeviceTypeCreateSchema,
        device_type_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await device_type_uow.update(id=id, update_object=form_data)
    except DeviceTypeDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_type_router.delete("/{id}", tags=['Device Types'])
async def delete_device_type(
        id: int,
        device_type_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await device_type_uow.delete(id=id)
    except DeviceTypeDoesNotExistsException as e:
        return
