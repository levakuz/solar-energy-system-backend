import abc
from typing import Type

from pydantic import BaseModel as PydanticModel

from src.core.models import BaseModel as DatabaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError


class TortoiseRepository(AbstractRepository):

    def __int__(
            self,
            model: Type[DatabaseModel],
            domain: Type[PydanticModel]
    ):
        self.model = model
        self.domain = domain

    async def get(self, **kwargs) -> PydanticModel:
        db_model = await self.model.get(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def delete(self, *args, **kwargs):
        pass

    async def add(self, *args, **kwargs) -> PydanticModel:
        db_model = await self.model.create(**kwargs, phone_number='123')
        return self.domain.parse_obj(db_model.__dict__)

    async def list(self, *args, **kwargs):
        pass
