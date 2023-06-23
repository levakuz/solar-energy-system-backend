from typing import Annotated, List

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.exceptions import DeviceEnergyDoesNotExistsException
from src.device_energies.schemas import DeviceEnergyCreateSchema, DeviceEnergyFilterSchema
from src.device_energies.unit_of_work import DeviceEnergyUnitOfWork

device_energy_router = fastapi.routing.APIRouter(
    prefix='/device-energies'
)


@device_energy_router.post("", response_model=DeviceEnergy, tags=['Device Energies'])
async def create_device_energy(
        form_data: DeviceEnergyCreateSchema,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    return await device_energy_uow.add(**form_data.dict())


@device_energy_router.get("", response_model=PaginationSchema[DeviceEnergy], tags=['Device Energies'])
async def get_device_energy_list(
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
        filters: Annotated[DeviceEnergyFilterSchema, Depends(DeviceEnergyFilterSchema)],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)]
):
    devices = await device_energy_uow.list(**filters.dict(), **pagination.dict())
    count = await device_energy_uow.count(**filters.dict())
    paginator = Paginator[DeviceEnergy](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@device_energy_router.get("/{id}", response_model=DeviceEnergy, tags=['Device Energies'])
async def get_device_energy(
        id: int,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    try:
        return await device_energy_uow.get(id=id)
    except DeviceEnergyDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_energy_router.put("/{id}", response_model=DeviceEnergy, tags=['Device Energies'])
async def update_device_energy(
        id: int,
        form_data: DeviceEnergyCreateSchema,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    try:
        return await device_energy_uow.update(id=id, update_object=form_data)
    except DeviceEnergyDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@device_energy_router.delete("/{id}", tags=['Device Energies'])
async def delete_device_energy(
        id: int,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    try:
        return await device_energy_uow.delete(id=id)
    except DeviceEnergyDoesNotExistsException as e:
        return
