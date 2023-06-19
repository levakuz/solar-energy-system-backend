from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_types.domain import DeviceType
from src.device_types.exceptions import DeviceTypeDoesNotExistsException
from src.device_types.schemas import DeviceTypeCreateSchema
from src.device_types.unit_of_work import DeviceTypeUnitOfWork

device_type_router = fastapi.routing.APIRouter(
    prefix='/device-types'
)


@device_type_router.post("", response_model=DeviceType, tags=['Device Types'])
async def create_device_type(
        form_data: DeviceTypeCreateSchema,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    return await company_account_uow.add(**form_data.dict())


@device_type_router.get("/{id}", response_model=DeviceType, tags=['Device Types'])
async def get_device_type(
        id: int,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await company_account_uow.get(id=id)
    except DeviceTypeDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_type_router.put("/{id}", response_model=DeviceType, tags=['Device Types'])
async def update_device_type(
        id: int,
        form_data: DeviceTypeCreateSchema,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await company_account_uow.update(id=id, update_object=form_data)
    except DeviceTypeDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_type_router.delete("/{id}", tags=['Device Types'])
async def delete_device_type(
        id: int,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceTypeUnitOfWork)
        ],
):
    try:
        return await company_account_uow.delete(id=id)
    except DeviceTypeDoesNotExistsException as e:
        return
