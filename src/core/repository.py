import abc
from typing import TypeVar, Generic, List, NoReturn, Callable

from pydantic import BaseModel as PydanticModel, BaseModel
from tortoise.queryset import QuerySet

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

    @abc.abstractmethod
    async def count(self, *args, **kwargs):
        raise NotImplementedError


def process_filter(func: Callable):
    async def wrapper(*args, **kwargs):
        for key in list(kwargs):
            if kwargs[key] is None:
                kwargs.pop(key)
        return await func(*args, **kwargs)

    return wrapper


class TortoiseRepository(AbstractRepository):

    def __init__(
            self,
            domain: T
    ):
        self.domain = domain

    async def get(self, *args, **kwargs) -> T:
        db_model = await self.domain.__config__.db_model.get(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def delete(self, *args, **kwargs) -> NoReturn:
        db_model = await self.domain.__config__.db_model.get(**kwargs)
        await db_model.delete()
        await db_model.save()

    async def add(self, *args, **kwargs) -> T:
        db_model = await self.domain.__config__.db_model.create(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    @process_filter
    async def list(self, limit: int = 0, offset: int = 0, *args, **kwargs) -> List[T]:
        db_models = QuerySet(self.domain.__config__.db_model)
        if limit or offset:
            db_models = db_models.filter(*args, **kwargs)
            db_models = await db_models.limit(limit).offset(offset)
        else:
            db_models = await db_models.filter(*args, **kwargs)
        return [self.domain.parse_obj(model.__dict__) for model in db_models]

    async def update(self, update_object: PydanticModel, **kwargs) -> T:
        return await self.domain.__config__.db_model.get(**kwargs).update(**update_object.dict())

    @process_filter
    async def count(self, limit: int = 0, offset: int = 0, *args, **kwargs) -> int:
        db_models = QuerySet(self.domain.__config__.db_model)
        db_models = db_models.filter(*args, **kwargs)
        return await db_models.count()


class BeanieRepository(AbstractRepository):

    def __init__(
            self,
            domain: T
    ):
        self.domain = domain

    async def get(self, *args, **kwargs) -> T | None:
        db_model = await self.domain.__config__.db_model.find_one(kwargs)
        if db_model is not None:
            return self.domain.parse_obj(db_model.__dict__)
        return db_model

    async def delete(self, *args, **kwargs) -> NoReturn:
        db_model = await self.domain.__config__.db_model.find_one(*args, **kwargs)
        await db_model.delete()

    async def add(self, *args, **kwargs) -> T:
        db_model = await self.domain.__config__.db_model.insert(**kwargs)
        return self.domain.parse_obj(db_model.__dict__)

    async def list(self, *args, **kwargs):
        pass

    async def update(self, update_object: PydanticModel, **kwargs) -> T:
        return await self.domain.__config__.db_model.find_one(**kwargs).update(**update_object.dict())

    async def count(self, *args, **kwargs):
        pass
