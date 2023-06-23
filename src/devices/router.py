from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.core.pagination import Paginator
from src.core.schemas import PaginationSchema, PaginationRequestSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.devices.domain import Device
from src.devices.exceptions import DeviceDoesNotExistsException
from src.devices.schemas import DeviceCreateUpdateSchema, DeviceFilterSchema
from src.devices.unit_of_work import DeviceUnitOfWork

device_router = fastapi.routing.APIRouter(
    prefix='/devices'
)


@device_router.post("", response_model=Device, tags=['Devices'])
async def create_device(
        form_data: DeviceCreateUpdateSchema,
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
):
    return await device_uow.add(**form_data.dict())


@device_router.get("", response_model=PaginationSchema[Device], tags=['Devices'])
async def get_devices_list(
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
        filters: Annotated[DeviceFilterSchema, Depends(DeviceFilterSchema)],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    devices = await device_uow.list(**filters.dict(), **pagination.dict())
    count = await device_uow.count(**filters.dict(), **pagination.dict())
    paginator = Paginator[Device](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@device_router.get("/{id}", response_model=Device, tags=['Devices'])
async def get_device(
        id: int,
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
):
    try:
        return await device_uow.get(id=id)
    except DeviceDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_router.put("/{id}", response_model=Device, tags=['Devices'])
async def update_device(
        id: int,
        form_data: DeviceCreateUpdateSchema,
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
):
    try:
        return await device_uow.update(id=id, update_object=form_data)
    except DeviceDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_router.delete("/{id}", tags=['Devices'])
async def delete_device(
        id: int,
        device_uow: Annotated[
            AbstractUnitOfWork[Device],
            Depends(DeviceUnitOfWork)
        ],
):
    try:
        return await device_uow.delete(id=id)
    except DeviceDoesNotExistsException:
        return
