from typing import Annotated

from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.locations.domain import Location
from src.locations.schemas import LocationCreateUpdateSchema
from src.locations.unit_of_work import LocationUnitOfWork


async def create_location(
        location: LocationCreateUpdateSchema,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
) -> Location:
    return await location_uow.add(**location.dict())