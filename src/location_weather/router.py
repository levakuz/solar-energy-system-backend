from typing import Annotated

import fastapi
from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_types.domain import DeviceType
from src.device_types.schemas import DeviceTypeCreateSchema
from src.device_types.unit_of_work import DeviceTypeUnitOfWork
from src.location_weather.domain import LocationWeather
from src.location_weather.unit_of_work import LocationWeatherUnitOfWork

location_weather_router = fastapi.routing.APIRouter(
    prefix='/weather-locations'
)


@location_weather_router.post("", response_model=LocationWeather, tags=['Location Weather'])
async def create_location_weather(
        form_data: LocationWeather,
        location_weather_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationWeatherUnitOfWork)
        ],
):
    return await location_weather_uow.add(**form_data.dict())


@location_weather_router.get("/{location_id}", response_model=LocationWeather, tags=['Location Weather'])
async def get_location_weather(
        location_id: int,
        location_weather_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationWeatherUnitOfWork)
        ],
):
    return await location_weather_uow.get({"location_id": location_id})


@location_weather_router.put("/{location_id}", response_model=LocationWeather, tags=['Location Weather'])
async def update_location_weather(
        location_id: int,
        form_data: LocationWeather,
        location_weather_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationWeatherUnitOfWork)
        ],
):
    return await location_weather_uow.update(id=id, update_object=form_data)


@location_weather_router.delete("/{id}", tags=['Location Weather'])
async def delete_location_weather(
        id: int,
        location_weather_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationWeatherUnitOfWork)
        ],
):
    return await location_weather_uow.delete(id=id)
