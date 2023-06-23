from typing import Annotated, NoReturn

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.pagination import Paginator
from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.schemas import PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork
from src.reports.domain import Report
from src.reports.exceptions import ReportDoesNotExistsException


class ReportUnitOfWork(AbstractUnitOfWork[Report]):
    def __init__(
            self,
            report_repository: Annotated[
                AbstractRepository[Report],
                Depends(RepositoryFactory(
                    domain_model=Report,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._report_repository = report_repository

    async def get(self, *args, **kwargs) -> Report:
        try:
            return await self._report_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise ReportDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> Report:
        try:
            await self._report_repository.update(update_object=update_object, **kwargs)
            return await self._report_repository.get(**kwargs)
        except DoesNotExist as e:
            raise ReportDoesNotExistsException

    async def add(self, *args, **kwargs) -> Report:
        return await self._report_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        try:
            await self._report_repository.delete(*args, **kwargs)
        except DoesNotExist as e:
            raise ReportDoesNotExistsException

    async def list(self, *args, **kwargs) -> PaginationSchema[Report]:
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        devices, count = await self._report_repository.list(limit=limit, offset=offset, *args, **kwargs)
        paginator = Paginator[Report](limit=limit, offset=offset, models_list=devices, count=count)
        return await paginator.get_response()
