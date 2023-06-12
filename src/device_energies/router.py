from typing import Annotated

import fastapi
from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.schemas import DeviceEnergyCreateSchema
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


@device_energy_router.get("/{id}", response_model=DeviceEnergy, tags=['Device Energies'])
async def get_device_energy(
        id: int,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    return await device_energy_uow.get(id=id)


@device_energy_router.put("/{id}", response_model=DeviceEnergy, tags=['Device Energies'])
async def update_device_energy(
        id: int,
        form_data: DeviceEnergyCreateSchema,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    return await device_energy_uow.update(id=id, update_object=form_data)


@device_energy_router.delete("/{id}", tags=['Device Energies'])
async def delete_device_energy(
        id: int,
        device_energy_uow: Annotated[
            AbstractUnitOfWork,
            Depends(DeviceEnergyUnitOfWork)
        ],
):
    return await device_energy_uow.delete(id=id)
