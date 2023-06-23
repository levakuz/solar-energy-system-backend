from functools import cached_property
from typing import TypeVar, Generic, List

from tortoise import Model

from src.core.middlewares.pagination import request_object
from src.core.schemas import PaginationSectionSchema, PaginationSchema

T = TypeVar("T", bound=Model)


class Paginator(Generic[T]):

    def __init__(
            self,
            models_list: List[T],
            limit: int,
            offset: int,
            count: int
    ):
        self.models_list = models_list
        self.limit = limit
        self.offset = offset
        self.request = request_object.get()
        self.count = count

    @cached_property
    def _total_pages(self) -> int:
        total_pages = self.count // self.limit
        return total_pages if total_pages != 0 else 1

    async def _get_next_page(self):
        if self.offset + 1 < self._total_pages:
            return str(self.request.url.include_query_params(offset=self.offset + 1))

    def _get_prev_page(self):
        if self.offset != 0:
            return str(self.request.url.include_query_params(offset=self.offset - 1))

    def _get_last_page(self):
        if self._total_pages != 1:
            return str(self.request.url.include_query_params(limit=self.limit, offset=self._total_pages - 1))
        else:
            return str(str(self.request.url.include_query_params(limit=self.limit, offset=self._total_pages)))

    async def _get_pagination_section(self) -> PaginationSectionSchema:
        return PaginationSectionSchema(
            limit=self.limit,
            offset=self.offset,
            totalPages=self._total_pages,
            next=await self._get_next_page(),
            prev=self._get_prev_page(),
            last=self._get_last_page()

        )

    async def get_response(self) -> PaginationSchema:
        return PaginationSchema(
            pagination=await self._get_pagination_section(),
            items=self.models_list
        )
