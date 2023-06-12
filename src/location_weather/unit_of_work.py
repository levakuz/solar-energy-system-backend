from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel

from src.core.repository import AbstractRepository, BeanieRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.location_weather.domain import LocationWeather


class LocationWeatherUnitOfWork(AbstractUnitOfWork[LocationWeather]):
    def __init__(
            self,
            location_weather_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=LocationWeather,
                    type_repository=BeanieRepository
                ))
            ],
    ):
        self._location_weather_repository = location_weather_repository

    async def get(self, *args, **kwargs) -> LocationWeather:
        return await self._location_weather_repository.get(*args, **kwargs)

    async def update(self, update_object: BaseModel, **kwargs) -> LocationWeather:
        return await self._location_weather_repository.update(update_object=update_object, **kwargs)

    async def add(self, *args, **kwargs) -> LocationWeather:
        return await self._location_weather_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self._location_weather_repository.delete(*args, **kwargs)
