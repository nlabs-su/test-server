"""
Модуль запросов к БД.
"""
import datetime

import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.db.exceptions import DBInstanceError
from app.lib.crypt import get_password_hash, generate_password


async def user_create(session: AsyncSession,) -> (models.User, str):
    """Функция добавления пользователя в БД.

    :param session: Объект Session.

    :return: Объект User.
    """
    first_name = ['Иван', 'Анастасия']
    last_name = ['Петров', 'Сидорова']

    tags_names = ["Работа", "Учеба", "Хобби"]

    date = datetime.datetime.today().date()

    tasks = [
        {
            'name': 'Начать читать книгу `Чистый код` Роберта Мартина',
            'description': None,
            'date': date,
            'type': models.Type.COMPLETED.value,
            'user_id': None,
            'timestamp': None,
            'tags': [3]
        },
        {
            'name': 'Найти белые грибы',
            'description': None,
            'date': date,
            'type': models.Type.IN_PROGRESS.value,
            'user_id': None,
            'timestamp': None,
            'tags': [3]
        },
        {
            'name': 'Купить билеты в КНР',
            'description': None,
            'date': date,
            'type': models.Type.COMPLETED.value,
            'user_id': None,
            'timestamp': None,
            'tags': []
        },
        {
            'name': 'Собеседование в Google в 17:25',
            'description': 'Уточнить информацию у Сергея Брина',
            'date': date + datetime.timedelta(days=2),
            'type': models.Type.ADDED.value,
            'user_id': None,
            'timestamp': None,
            'tags': [1]
        },
        {
            'name': 'Решить задачу "Равенства классов P и NP"',
            'description': 'Проблема равенства этих классов является одной из важнейших проблем теории алгоритмов.',
            'date': date + datetime.timedelta(days=3),
            'type': models.Type.ADDED.value,
            'user_id': None,
            'timestamp': None,
            'tags': []
        },
        {
            'name': 'Посмотреть фильм "Москва слезам не верит"',
            'description': None,
            'date': date + datetime.timedelta(days=3),
            'type': models.Type.ADDED.value,
            'user_id': None,
            'timestamp': None,
            'tags': []
        },
        {
            'name': 'Сеанс у стоматолога',
            'description': 'Прийти к стоматологу в клинику DentGoldBlackPower',
            'date': date + datetime.timedelta(days=6),
            'type': models.Type.ADDED.value,
            'user_id': None,
            'timestamp': None,
            'tags': []
        },
    ]

    users_count = await session.scalar(sa.select(sa.func.count(models.User.id)))
    c = (users_count + 1) % 2

    password = generate_password()

    user = models.User(
        login=f'user{users_count + 1}',
        password=await get_password_hash(password),
        last_name=last_name[c],
        first_name=first_name[c]
    )
    session.add(user)

    await session.flush()

    for tag_name in tags_names:
        tag = models.Tag(
            name=tag_name,
            user_id=user.id
        )
        session.add(tag)

        await session.flush()

    for t, _task in enumerate(tasks):
        timestamp = datetime.datetime.now() + datetime.timedelta(minutes=t)
        task = models.Task(
            name=_task['name'],
            description=_task['description'],
            date=_task['date'],
            type=_task['type'],
            user_id=user.id,
            timestamp=timestamp
        )
        session.add(task)

        await session.flush()

        for tag_id in _task['tags']:
            tag_task = models.TaskTag(
                task_id=task.id,
                tag_id=tag_id
            )
            session.add(tag_task)

            await session.flush()

    await session.commit()

    return user, password


async def user_read(
        session: AsyncSession,
        id: int = None,
        login: str = None,
) -> models.User:
    """Функция получения объекта аккаунта из БД.

    :param session: Объект Session.

    :param id: Идентификатор пользователя.
    :param login: Логин.

    :return: Объект User.
    """
    query = sa.select(models.User)
    if id:
        query = query.where(models.User.id == id)
    if login:
        query = query.where(models.User.login == login)

    user = await session.scalar(query)

    return user


async def tag_create(
        session: AsyncSession,
        name: str,
        user_id: int
) -> models.Tag:
    """Функция добавления тега в БД.

    :param session: Объект Session.
    :param name: Название.
    :param user_id: Идентификатор пользователя.

    :return: Объект Tag.
    """
    tag = models.Tag(name=name, user_id=user_id)

    session.add(tag)

    await session.commit()

    return tag


async def tag_read(
        session: AsyncSession,
        id: int = None,
        name: str = None,
        user_id: int = None
) -> models.Tag:
    """Функция получения объекта тега из БД.

    :param session: Объект Session.
    :param id: Идентификатор задачи.
    :param name: Название.
    :param user_id: Идентификатор пользователя.

    :return: Объект Tag.
    """
    query = sa.select(models.Tag)

    if id:
        query = query.where(models.Tag.id == id)
    if name:
        query = query.where(models.Tag.name == name)
    if user_id:
        query = query.where(models.Tag.user_id == user_id)

    tag = await session.scalar(query)

    return tag


async def tags_read(
        session: AsyncSession,
        user_id: int
) -> list[models.Tag]:
    """Функция получения объектов тега из БД.

    :param session: Объект Session.
    :param user_id: Идентификатор пользователя.

    :return: Список объектов Task.
    """
    query = sa.select(models.Tag).where(models.Tag.user_id == user_id,).order_by(models.Tag.name)

    tags = (await session.scalars(query)).all()

    return tags


async def tag_update(
        session: AsyncSession,
        tag: models.Tag,
        name: str
):
    """Функция изменения данных тега.

    :param session: Объект Session.
    :param tag: Объект models.Tag.
    :param name: Название.
    """
    tag.name = name
    await session.commit()


async def tag_delete(session: AsyncSession, tag: models.Tag) -> None:
    """Функция удаления тега.

    :param session: Объект Session.
    :param tag: Объект models.Tag.
    """
    if not isinstance(tag, models.Tag):
        raise DBInstanceError(tag, models.Tag())

    await session.delete(tag)
    await session.commit()


async def task_create(
        session: AsyncSession,
        name: str,
        description: str,
        date: datetime.date,
        type: models.Type,
        user_id: int,
        tags: list[int]
) -> models.Task:
    """Функция добавления задачи в БД.

    :param session: Объект Session.
    :param name: Название.
    :param description: Описание.
    :param date: Дата.
    :param type: Тип.
    :param user_id: Идентификатор пользователя.
    :param tags: Список идентификаторов тегов.

    :return: Объект Task.
    """
    task = models.Task(
        name=name,
        description=description,
        date=date,
        type=type,
        user_id=user_id
    )

    session.add(task)

    await session.flush()

    task_tags = []
    for tag_id in tags:
        task_tags.append(models.TaskTag(tag_id=tag_id, task_id=task.id))

    if task_tags:
        session.add_all(task_tags)

    await session.commit()

    return task


async def task_read(
        session: AsyncSession,
        id: int = None,
        name: str = None,
        description: str = None,
        date: datetime.date = None,
        type: models.Type = None,
        user_id: int = None
) -> models.Task:
    """Функция получения объекта задачи из БД.

    :param session: Объект Session.
    :param id: Идентификатор задачи.
    :param name: Название.
    :param description: Описание.
    :param date: Дата.
    :param type: Тип.
    :param user_id: Идентификатор пользователя.

    :return: Объект Task.
    """
    query = sa.select(models.Task).options(
        sa.orm.joinedload(models.Task.user),
        sa.orm.selectinload(models.Task.tags)
    )

    if id:
        query = query.where(models.Task.id == id)
    if name:
        query = query.where(models.Task.name == name)
    if description:
        query = query.where(models.Task.description == description)
    if date:
        query = query.where(models.Task.date == date)
    if type:
        query = query.where(models.Task.type == type)
    if user_id:
        query = query.where(models.Task.user_id == user_id)

    task = await session.scalar(query)

    return task


async def tasks_read(
        session: AsyncSession,
        user_id: int,
        start_date: datetime.date,
        end_date: datetime.date
) -> list[models.Task]:
    """Функция получения объектов задач из БД.

    :param session: Объект Session.
    :param user_id: Идентификатор пользователя.
    :param start_date: Дата начала.
    :param end_date: Дата окончания.

    :return: Список объектов Task.
    """
    query = sa.select(models.Task).options(
        sa.orm.joinedload(models.Task.user),
        sa.orm.selectinload(models.Task.tags)
    ).where(
        models.Task.user_id == user_id,
        models.Task.date >= start_date,
        models.Task.date <= end_date
    ).order_by(models.Task.timestamp)

    tasks = (await session.scalars(query)).all()

    return tasks


async def task_update(
        session: AsyncSession,
        task: models.Task,
        name: str,
        description: str,
        date: datetime.date,
        type: models.Type,
        tags: list[int]
):
    """Функция изменения данных задачи.

    :param session: Объект Session.
    :param task: Объект models.Task.
    :param name: Название.
    :param description: Описание.
    :param date: Дата.
    :param type: Тип.
    :param tags: Список идентификаторов тегов.
    """
    task.name = name
    task.description = description
    task.date = date
    task.type = type

    await task_tags_delete(session=session, task_id=task.id)

    task_tags = []
    for tag_id in tags:
        task_tags.append(models.TaskTag(tag_id=tag_id, task_id=task.id))

    if task_tags:
        session.add_all(task_tags)

    await session.commit()


async def task_tags_delete(session: AsyncSession, task_id: int) -> None:
    """Функция удаления тегов задачи.

    :param session: Объект Session.
    :param task_id: Идентификатор задачи.
    """
    await session.execute(sa.delete(models.TaskTag).where(models.TaskTag.task_id == task_id))
    await session.commit()


async def task_delete(session: AsyncSession, task: models.Task) -> None:
    """Функция удаления задачи.

    :param session: Объект Session.
    :param task: Объект models.Task.
    """
    if not isinstance(task, models.Task):
        raise DBInstanceError(task, models.Task())

    await task_tags_delete(session=session, task_id=task.id)
    await session.delete(task)
    await session.commit()
