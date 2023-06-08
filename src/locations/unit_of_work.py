from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.locations.domain import Location
from src.locations.exceptions import LocationDoesNotExistsException


class LocationUnitOfWork(AbstractUnitOfWork[Location]):
    def __init__(
            self,
            location_repository: Annotated[
                AbstractRepository[Location],
                Depends(RepositoryFactory(
                    domain_model=Location,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._location_repository = location_repository

    async def get(self, *args, **kwargs) -> Location:
        try:
            return await self._location_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise LocationDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> Location:
        try:
            await self._location_repository.update(update_object=update_object, **kwargs)
            return await self._location_repository.get(**kwargs)
        except DoesNotExist as e:
            raise LocationDoesNotExistsException

    async def add(self, *args, **kwargs) -> Location:
        return await self._location_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._location_repository.delete(*args, **kwargs)
