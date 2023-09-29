"""
Модуль авторизации.
"""
from typing import Any

from litestar import Request
from litestar.connection import ASGIConnection
from litestar.contrib.jwt import Token, JWTAuth

from app import db
from app.lib import settings
from app.domain import urls


async def provide_user(request: Request[db.models.User, Token, Any]) -> db.models.User:
    """Функция получения аккаунта сотрудника из запроса.

    :param request: Запрос.

    :return: models.User: Пользователь.
    """
    return request.user


async def current_user_from_token(
        token: "Token", connection: "ASGIConnection[Any, Any, Any, Any]"  # noqa
) -> db.models.User | None:
    """Функция получения текущего пользователя по JWT токену.

    Извлекает пользователя из БД.

    :param token: Объект JWT токена.
    :param connection: ASGI соединение.

    :return: models.User: Объект пользователя.
    """
    async with db.Session() as session:
        user = await db.queries.user_read(
            session=session,
            id=token.sub
        )
    if not user:
        return None

    return user


auth = JWTAuth[db.models.User](
    retrieve_user_handler=current_user_from_token,
    token_secret=settings.app.SECRET_KEY,
    exclude=[
        ''.join([urls.BASE_API_PATH, urls.USER_LOGIN]),
        ''.join([urls.BASE_API_PATH, urls.USER_CREATE]),
        urls.OPENAPI_SCHEMA
    ]
)
