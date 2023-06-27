from typing import Annotated, NoReturn

import httpx
from fastapi import Depends

from src.core.scheduler import service_scheduler
from src.core.unit_of_work import AbstractUnitOfWork
from src.locations.domain import Location
from src.locations.exceptions import GeocodingNotFoundException
from src.locations.schemas import LocationCreateUpdateSchema, LocationGeocodingResponseSchema, \
    LocationGeocodingAPIResponseSchema
from src.locations.tasks import get_weather_for_last_day
from src.locations.unit_of_work import LocationUnitOfWork


async def create_location(
        location: LocationCreateUpdateSchema,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
) -> Location:
    created_location = await location_uow.add(**location.dict())
    service_scheduler.add_job(
        get_weather_for_last_day,
        'interval',
        days=1,
        id=f'location__{created_location.id}',
        args=[location.latitude, location.longitude, created_location.id],
    )  # TODO: Business logic now depends on tasks (?)
    return created_location


async def get_location_by_name(name: str) -> LocationGeocodingResponseSchema:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en&format=json'
        )
        parsed_response = LocationGeocodingAPIResponseSchema.parse_obj(response.json())
    if not parsed_response.results:
        raise GeocodingNotFoundException
    return LocationGeocodingResponseSchema.parse_obj(parsed_response.results[0])


async def try_to_delete_location(
        location_uow: AbstractUnitOfWork[Location],
        location_id: int
) -> NoReturn:
    await location_uow.delete(id=location_id)
    service_scheduler.remove_job(f'location__{location_id}')