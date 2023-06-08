from typing import Annotated

import fastapi
from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.locations import services
from src.locations.domain import Location
from src.locations.schemas import LocationCreateUpdateSchema
from src.locations.unit_of_work import LocationUnitOfWork

locations_router = fastapi.routing.APIRouter(
    prefix='/locations'
)


@locations_router.post("", response_model=Location, tags=['Locations'])
async def create_location(
        form_data: LocationCreateUpdateSchema,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
):
    return await services.create_location(form_data, location_uow)


@locations_router.get("/{id}", response_model=Location, tags=['Locations'])
async def get_location(
        id: int,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
):
    return await location_uow.get(id=id)


@locations_router.put("/{id}", response_model=Location, tags=['Locations'])
async def update_location(
        id: int,
        form_data: LocationCreateUpdateSchema,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
):
    return await location_uow.update(id=id, update_object=form_data)


@locations_router.delete("/{id}", tags=['Locations'])
async def delete_location(
        id: int,
        location_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationUnitOfWork)
        ],
):
    return await location_uow.delete(id=id)
