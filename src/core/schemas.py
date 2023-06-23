from typing import List, TypeVar, Generic, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T", bound=BaseModel)


class PaginationSectionSchema(BaseModel):
    limit: int
    offset: int
    totalPages: int
    next: Optional[str]
    prev: Optional[str]
    last: str


class PaginationSchema(GenericModel, Generic[T]):
    pagination: PaginationSectionSchema
    items: List[T]


class PaginationRequestSchema(BaseModel):
    limit: int = 10
    offset: int = 0
