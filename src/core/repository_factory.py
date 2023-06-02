import abc
from typing import Type, TypeVar

from pydantic import BaseModel

from src.core.repository import AbstractRepository

T = TypeVar("T", bound=BaseModel)

class AbstractRepositoryFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryFactory(AbstractRepositoryFactory):
    def __init__(
            self,
            domain_model: Type[T],
            type_repository: Type[AbstractRepository]
    ):
        self.domain_model = domain_model
        self.repository_type = type_repository

    def __call__(self) -> AbstractRepository[T]:
        return self.repository_type(self.domain_model)
