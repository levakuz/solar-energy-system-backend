import abc
from typing import TypeVar, Generic, List, NoReturn

from pydantic import BaseModel as PydanticModel, BaseModel

T = TypeVar("T", bound=BaseModel)


class AbstractRepository(Generic[T], abc.ABC):
    @abc.abstractmethod
    def __init__(self, domain: T):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self, *args, **kwargs) -> List[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    async def add(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, update_object: PydanticModel, **kwargs) -> T:
        raise NotImplementedError


class TortoiseRepository(AbstractRepository):

    def __init__(
            self,
            domain: T
    ):
        self.domain = domain

    async def get(self, **kwargs) -> T:
        db_model = await self.domain.__config__.db_model.get(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def delete(self, *args, **kwargs) -> NoReturn:
        await self.domain.__config__.db_model.delete(**kwargs)

    async def add(self, *args, **kwargs) -> T:
        db_model = await self.domain.__config__.db_model.create(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def list(self, *args, **kwargs):
        pass

    async def update(self, update_object: PydanticModel, **kwargs) -> T:
        return await self.domain.__config__.db_model.get(**kwargs).update(**update_object.dict())
