"""
Модуль исключений.
"""
from enum import IntEnum

from litestar import Request, Response


class APIError(Exception):
    def __init__(self, status_code: IntEnum, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


def api_error_handler(request: Request, exc: APIError) -> Response:
    return Response(
        content={
            "detail": exc.detail,
            "status_code": exc.status_code.value,
        },
        status_code=exc.status_code.value,
    )
