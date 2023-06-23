from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

request_object: ContextVar[Request] = ContextVar('request')


# https://lewoudar.medium.com/fastapi-and-pagination-d27ad52983a

class PaginationMiddleware(BaseHTTPMiddleware):
    """
    Middleware adds request in contextvars
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_object.set(request)
        response = await call_next(request)
        return response
