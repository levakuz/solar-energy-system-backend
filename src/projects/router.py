from typing import Annotated

import fastapi
from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork
from src.projects.domain import Project
from src.projects.schemas import ProjectCreateUpdateSchema
from src.projects.unit_of_work import ProjectUnitOfWork

project_router = fastapi.routing.APIRouter(
    prefix='/projects'
)


@project_router.post("", response_model=Project, tags=['Projects'])
async def create_project(
        form_data: ProjectCreateUpdateSchema,
        user_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    return await user_account_uow.add(**form_data.dict())


@project_router.get("/{id}", response_model=Project, tags=['Projects'])
async def get_project(
        id: int,
        user_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    return await user_account_uow.get(id=id)


@project_router.put("/{id}", response_model=Project, tags=['Projects'])
async def update_project(
        id: int,
        form_data: ProjectCreateUpdateSchema,
        user_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    return await user_account_uow.update(id=id, update_object=form_data)


@project_router.delete("/{id}", tags=['Projects'])
async def delete_project(
        id: int,
        user_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(ProjectUnitOfWork)
        ],
):
    return await user_account_uow.delete(id=id)
