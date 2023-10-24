"""
Контроллер API задач.
"""
import datetime
from http import HTTPStatus

from litestar import (
    Controller, post, get,
    put, delete
)
from sqlalchemy.exc import DBAPIError

from app import db
from app.domain import schemas, codes, urls
from app.domain.exceptions import APIError
from app.domain.tasks import schemas as controller_schemas


class TaskController(Controller):
    tags = ["Task"]

    @post(path=urls.TASKS_CREATE)
    async def create(
            self,
            data: controller_schemas.TaskCreate,
            current_user: db.models.User
    ) -> int | None:
        """
        API добавления задачи.

        Поле tags должно содержать идентификаторы тегов.

        - Если тег не существует, то вернется код `TAG_NOT_FOUND`.
        """
        async with db.Session() as session:
            for tag_id in data.tags:
                tag = await db.queries.tag_read(session=session, id=tag_id, user_id=current_user.id)
                if not tag:
                    raise APIError(HTTPStatus.BAD_REQUEST, codes.TAG_NOT_FOUND)

            try:
                task = await db.queries.task_create(session=session, user_id=current_user.id, **data.model_dump())
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return task.id

    @get(path=urls.TASKS_READ_BY_ID)
    async def read(
            self,
            id: int,
            current_user: db.models.User
    ) -> controller_schemas.Task | None:
        """
        API получения данных задачи по идентификатору.
        """
        async with db.Session() as session:
            task = await db.queries.task_read(session=session, user_id=current_user.id, id=id)
            if not task:
                raise APIError(HTTPStatus.NOT_FOUND, codes.NOT_FOUND)

        return controller_schemas.Task.model_validate(task)

    @get(path=urls.TASKS_READ)
    async def read_list(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            current_user: db.models.User
    ) -> controller_schemas.ReadTasks | None:
        """
        API получения данных задач пользователя.
        """
        async with db.Session() as session:
            tasks = await db.queries.tasks_read(
                session=session, user_id=current_user.id, start_date=start_date, end_date=end_date
            )

        return controller_schemas.ReadTasks(result=tasks)

    @get(path=urls.TASKS_TYPES_READ)
    async def read_types_list(self,) -> dict:
        """
        API получения типов задач.
        """
        return db.models.Type.to_dict()

    @put(path=urls.TASKS_UPDATE)
    async def update(
            self,
            id: int,
            data: controller_schemas.TaskUpdate,
            current_user: db.models.User
    ) -> schemas.Code | None:
        """
        API изменения задачи по идентификатору.

        Поле tags должно содержать идентификаторы тегов.

        - Если тег не существует, то вернется код `TAG_NOT_FOUND`.
        """
        async with db.Session() as session:
            task = await db.queries.task_read(session=session, id=id)
            if not task:
                raise APIError(HTTPStatus.NOT_FOUND, codes.NOT_FOUND)

            for tag_id in data.tags:
                tag = await db.queries.tag_read(session=session, id=tag_id, user_id=current_user.id)
                if not tag:
                    raise APIError(HTTPStatus.BAD_REQUEST, codes.TAG_NOT_FOUND)

            try:
                await db.queries.task_update(
                    session=session,
                    task=task,
                    **data.model_dump()
                )
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return schemas.Code(code=codes.SUCCESS)

    @delete(path=urls.TASKS_DELETE, status_code=HTTPStatus.OK.value)
    async def delete(
            self,
            id: int,
            current_user: db.models.User
    ) -> None:
        """
        API удаления задачи по идентификатору.
        """
        async with db.Session() as session:
            try:
                task = await db.queries.task_read(session=session, user_id=current_user.id, id=id)
                if not task:
                    raise APIError(HTTPStatus.NOT_FOUND, codes.NOT_FOUND)

                await db.queries.task_delete(session=session, task=task)
            except DBAPIError:
                await session.rollback()

                raise APIError(HTTPStatus.BAD_REQUEST, codes.BAD_REQUEST)

        return schemas.Code(code=codes.SUCCESS)
