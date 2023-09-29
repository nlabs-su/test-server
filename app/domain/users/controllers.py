"""
Контроллер API авторизации пользователя.
"""
import datetime
from http import HTTPStatus

from litestar import Controller, post, get
from litestar.params import Body
from litestar.contrib.jwt import OAuth2Login, Token
from litestar.enums import RequestEncodingType
from sqlalchemy.exc import DBAPIError

from app import db
from app.lib import crypt, settings
from app.domain import codes, urls
from app.domain.exceptions import APIError
from app.domain.users import schemas as controller_schemas


class UserController(Controller):
    tags = ["User"]
    signature_namespace = {"OAuth2Login": OAuth2Login}

    @get(path=urls.USER_CREATE)
    async def generate(self) -> db.models.User:
        """
        API генерации нового пользователя.

        Данный запрос создает нового пользователя для дальнейшей работы с защищенными эндпоинтами.

        Логин и пароль необходимо записать, чтобы далее использовать для авторизации.

        `Рекомендуется использовать не более 4-х раз. Достаточно создать 2 пользователя.`
        """
        async with db.Session() as session:
            try:
                user, password = await db.queries.user_create(session=session)
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return {'login': user.login, 'password': password}

    @post(path=urls.USER_LOGIN)
    async def login(
            self,
            data: controller_schemas.UserLoginData = Body(media_type=RequestEncodingType.URL_ENCODED)
    ) -> controller_schemas.Token | None:
        """
        API авторизации пользователя.

        Возвращает JWT-токен, который необходимо в дальнейшем использовать в Headers для авторизации пользователя.

        Headers:
        `Authorization: Bearer <token>`
        """
        async with db.Session() as session:
            user = await db.queries.user_read(session=session, login=data.login)
            if user and await crypt.verify_password(plain_password=data.password, hashed_password=user.password):
                token = Token(
                    sub=str(user.id),
                    exp=datetime.datetime.now() + datetime.timedelta(minutes=settings.app.AUTH_TOKEN_EXPIRES_MINUTES),
                )
                encoded_token = token.encode(secret=settings.app.SECRET_KEY, algorithm=settings.app.AUTH_JWT_ALGORITHM)

                return controller_schemas.Token(token=encoded_token, type='Bearer')

        raise APIError(status_code=HTTPStatus.UNAUTHORIZED, detail=codes.INVALID_AUTHORIZATION)

    @get(path=urls.USER_PROFILE)
    async def account_me(self, current_user: db.models.User) -> controller_schemas.User:
        """
        API получения данных авторизованного пользователя.
        """
        return controller_schemas.User.model_validate(current_user)
