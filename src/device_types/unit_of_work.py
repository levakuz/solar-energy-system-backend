from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.accounts.domain import UserAccount
from src.accounts.exceptions import AccountDoesNotExistsException
from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_types.domain import DeviceType


class DeviceTypeUnitOfWork(AbstractUnitOfWork[DeviceType]):
    def __init__(
            self,
            device_type_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=DeviceType,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._device_type_repository = device_type_repository

    async def get(self, *args, **kwargs) -> DeviceType:
        try:
            return await self._device_type_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> DeviceType:
        try:
            await self._device_type_repository.update(update_object=update_object, **kwargs)
            return await self._device_type_repository.get(**kwargs)
        except DoesNotExist as e:
            raise AccountDoesNotExistsException

    async def add(self, *args, **kwargs) -> DeviceType:
        return await self._device_type_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._device_type_repository.delete(*args, **kwargs)
