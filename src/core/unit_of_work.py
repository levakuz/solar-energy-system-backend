import abc
from typing import NoReturn, TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class AbstractUnitOfWork(Generic[T], abc.ABC):

    async def get(self, *args, **kwargs) -> T:
        raise NotImplementedError

    async def update(self, update_object: BaseModel, **kwargs) -> T:
        raise NotImplementedError

    async def add(self, *args, **kwargs) -> T:
        raise NotImplementedError

    async def delete(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

    async def list(self, *args, **kwargs) -> List[T]:
        raise NotImplementedError
