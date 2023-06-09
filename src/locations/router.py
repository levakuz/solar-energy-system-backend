from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.auth.services import get_current_active_user
from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.locations import services
from src.locations.domain import Location
from src.locations.exceptions import LocationDoesNotExistsException, GeocodingNotFoundException
from src.locations.schemas import LocationCreateUpdateSchema, LocationGeocodingResponseSchema
from src.locations.services import get_location_by_name, try_to_delete_location
from src.locations.unit_of_work import LocationUnitOfWork

locations_router = fastapi.routing.APIRouter(
    prefix='/locations',
    dependencies=[Depends(get_current_active_user)],
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


@locations_router.get("", response_model=PaginationSchema[Location], tags=['Locations'])
async def get_locations_list(
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    devices = await location_uow.list(**pagination.dict())
    count = await location_uow.count()
    paginator = Paginator[Location](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@locations_router.get("/{id}", response_model=Location, tags=['Locations'])
async def get_location(
        id: int,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
):
    try:
        return await location_uow.get(id=id)
    except LocationDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@locations_router.put("/{id}", response_model=Location, tags=['Locations'])
async def update_location(
        id: int,
        form_data: LocationCreateUpdateSchema,
        location_uow: Annotated[
            AbstractUnitOfWork[Location],
            Depends(LocationUnitOfWork)
        ],
):
    try:
        return await location_uow.update(id=id, update_object=form_data)
    except LocationDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@locations_router.delete("/{id}", tags=['Locations'])
async def delete_location(
        id: int,
        location_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationUnitOfWork)
        ],
):
    try:
        await try_to_delete_location(location_uow=location_uow, location_id=id)
    except LocationDoesNotExistsException:
        return


@locations_router.get("/geocoding/", tags=['Locations'], response_model=LocationGeocodingResponseSchema)
async def get_location_by_coordinates(
        name: str,
        location_uow: Annotated[
            AbstractUnitOfWork,
            Depends(LocationUnitOfWork)
        ],
):
    try:
        return await get_location_by_name(name)
    except GeocodingNotFoundException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})
