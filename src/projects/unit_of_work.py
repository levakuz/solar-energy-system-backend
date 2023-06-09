import uuid
from typing import Annotated, NoReturn, List

from fastapi import Depends, UploadFile
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.projects.domain import Project
from src.projects.exceptions import ProjectDoesNotExistsException


class ProjectUnitOfWork(AbstractUnitOfWork[Project]):
    def __init__(
            self,
            project_repository: Annotated[
                AbstractRepository[Project],
                Depends(RepositoryFactory(
                    domain_model=Project,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._project_repository = project_repository

    async def get(self, *args, **kwargs) -> Project:
        try:
            return await self._project_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise ProjectDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> Project:
        try:
            await self._project_repository.update(update_object=update_object, **kwargs)
            return await self._project_repository.get(**kwargs)
        except DoesNotExist as e:
            raise ProjectDoesNotExistsException

    async def add(self, *args, **kwargs) -> Project:
        photo = kwargs.pop('photo')  # type: UploadFile
        file_name = f'{kwargs.get("name")}_{uuid.uuid4()}.png'
        with open(f'./src/staticfiles/projects_photos/{file_name}', 'wb') as file:
            data = await photo.read()
            file.write(data)
        kwargs['photo'] = file_name
        return await self._project_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        try:
            await self._project_repository.delete(*args, **kwargs)
        except DoesNotExist as e:
            raise ProjectDoesNotExistsException

    async def list(self, *args, **kwargs) -> List[Project]:
        return await self._project_repository.list(*args, **kwargs)

    async def count(self, *args, **kwargs) -> int:
        return await self._project_repository.count(*args, **kwargs)
