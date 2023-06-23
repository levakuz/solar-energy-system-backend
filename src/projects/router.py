from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.projects.domain import Project
from src.projects.exceptions import ProjectDoesNotExistsException
from src.projects.schemas import ProjectCreateUpdateSchema, ProjectFilterSchema
from src.projects.unit_of_work import ProjectUnitOfWork

project_router = fastapi.routing.APIRouter(
    prefix='/projects'
)


@project_router.post("", response_model=Project, tags=['Projects'])
async def create_project(
        form_data: ProjectCreateUpdateSchema,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    return await project_uow.add(**form_data.dict())


@project_router.get("", response_model=PaginationSchema[Project], tags=['Projects'])
async def get_projects_list(
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
        filters: Annotated[ProjectFilterSchema, Depends(ProjectFilterSchema)],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    devices = await project_uow.list(**filters.dict(), **pagination.dict())
    count = await project_uow.count(**filters.dict())
    paginator = Paginator[Project](models_list=devices, count=count, **pagination.dict())
    return await paginator.get_response()


@project_router.get("/{id}", response_model=Project, tags=['Projects'])
async def get_project(
        id: int,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.get(id=id)
    except ProjectDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@project_router.put("/{id}", response_model=Project, tags=['Projects'])
async def update_project(
        id: int,
        form_data: ProjectCreateUpdateSchema,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.update(id=id, update_object=form_data)
    except ProjectDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@project_router.delete("/{id}", tags=['Projects'])
async def delete_project(
        id: int,
        project_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    try:
        return await project_uow.delete(id=id)
    except ProjectDoesNotExistsException as e:
        return
