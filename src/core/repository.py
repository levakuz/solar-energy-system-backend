import abc
from typing import Type

from pydantic import BaseModel as PydanticModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, domain: Type[PydanticModel]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, *args, **kwargs) -> PydanticModel:
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

    def __init__(
            self,
            domain: Type[PydanticModel]
    ):
        self.domain = domain

    async def get(self, **kwargs) -> PydanticModel:
        db_model = await self.domain.__config__.db_model.get(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def delete(self, *args, **kwargs):
        db_model = await self.domain.__config__.db_model.delete(**kwargs)

    async def add(self, *args, **kwargs) -> PydanticModel:
        db_model = await self.domain.__config__.db_model.create(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def list(self, *args, **kwargs):
        pass
