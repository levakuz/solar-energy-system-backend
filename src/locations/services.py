from typing import Annotated

from fastapi import Depends

from src.core.scheduler import service_scheduler
from src.core.unit_of_work import AbstractUnitOfWork
from src.locations.domain import Location
from src.locations.schemas import LocationCreateUpdateSchema
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
        seconds=10,
        id=str(created_location.id),
        args=[location.latitude,location.longitude, created_location.id],
    )  # TODO: Business logic now depends on tasks (?)
    return created_location
