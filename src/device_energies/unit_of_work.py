from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.exceptions import DeviceEnergyDoesNotExistsException


class DeviceEnergyUnitOfWork(AbstractUnitOfWork[DeviceEnergy]):
    def __init__(
            self,
            device_energy_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=DeviceEnergy,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._device_energy_repository = device_energy_repository

    async def get(self, *args, **kwargs) -> DeviceEnergy:
        try:
            return await self._device_energy_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceEnergyDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> DeviceEnergy:
        try:
            await self._device_energy_repository.update(update_object=update_object, **kwargs)
            return await self._device_energy_repository.get(**kwargs)
        except DoesNotExist as e:
            raise DeviceEnergyDoesNotExistsException

    async def add(self, *args, **kwargs) -> DeviceEnergy:
        return await self._device_energy_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        try:
            await self._device_energy_repository.delete(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceEnergyDoesNotExistsException
