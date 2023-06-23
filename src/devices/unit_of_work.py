from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.pagination import Paginator
from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.schemas import PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.devices.domain import Device
from src.devices.exceptions import DeviceDoesNotExistsException


class DeviceUnitOfWork(AbstractUnitOfWork[Device]):
    def __init__(
            self,
            device_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=Device,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._device_repository = device_repository

    async def get(self, *args, **kwargs) -> Device:
        try:
            return await self._device_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> Device:
        try:
            await self._device_repository.update(update_object=update_object, **kwargs)
            return await self._device_repository.get(**kwargs)
        except DoesNotExist as e:
            raise DeviceDoesNotExistsException

    async def add(self, *args, **kwargs) -> Device:
        return await self._device_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        try:
            await self._device_repository.delete(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceDoesNotExistsException

    async def list(self, *args, **kwargs) -> PaginationSchema[Device]:
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        devices, count = await self._device_repository.list(limit=limit, offset=offset, *args, **kwargs)
        paginator = Paginator[Device](limit=limit, offset=offset, models_list=devices, count=count)
        return await paginator.get_response()
