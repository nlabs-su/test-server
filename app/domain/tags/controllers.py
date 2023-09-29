"""
Контроллер API тегов.
"""
from http import HTTPStatus

from litestar import (
    Controller, post, get,
    put, delete
)
from sqlalchemy.exc import DBAPIError

from app import db
from app.domain import schemas, codes, urls
from app.domain.exceptions import APIError
from app.domain.tags import schemas as controller_schemas


class TagController(Controller):
    tags = ["Tag"]

    @post(path=urls.TAGS_CREATE)
    async def create(
            self,
            data: controller_schemas.TagCreate,
            current_user: db.models.User
    ) -> int | None:
        """
        API добавления тега.
        """
        async with db.Session() as session:
            tag = await db.queries.tag_read(session=session, user_id=current_user.id, name=data.name)
            if tag:
                raise APIError(HTTPStatus.BAD_REQUEST, codes.TAG_ALREADY_EXISTS)

            try:
                tag = await db.queries.tag_create(session=session, user_id=current_user.id, name=data.name)
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return tag.id

    @get(path=urls.TAGS_READ)
    async def read_list(
            self,
            current_user: db.models.User
    ) -> controller_schemas.ReadTags | None:
        """
        API получения тегов, добавленных пользователем.
        """
        async with db.Session() as session:
            tags = await db.queries.tags_read(session=session, user_id=current_user.id)

        return controller_schemas.ReadTags(result=tags)

    @delete(path=urls.TAGS_DELETE, status_code=HTTPStatus.OK.value)
    async def delete(
            self,
            id: int,
            current_user: db.models.User
    ) -> None:
        """
        API удаления тега по идентификатору.
        """
        async with db.Session() as session:
            try:
                tag = await db.queries.tag_read(session=session, user_id=current_user.id, id=id)
                if not tag:
                    raise APIError(HTTPStatus.NOT_FOUND, codes.NOT_FOUND)

                await db.queries.tag_delete(session=session, tag=tag)
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return schemas.Code(code=codes.SUCCESS)
