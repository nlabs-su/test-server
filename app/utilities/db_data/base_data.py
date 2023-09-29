"""
Модуль инициализации базовых данных.
"""
import datetime

from app.db import models
from app.db.session import Session
from app.lib.crypt import get_password_hash


async def init_base_data() -> bool:
    """
    Функция инициализации базовых данных.
    """
    async with Session() as session:
        first_name = ['Иван', 'Анастасия']
        last_name = ['Петров', 'Сидорова']

        tags_names = ["Работа", "Учеба", "Хобби"]

        date = datetime.date(2023, 9, 27)

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

        for i in range(1, 101):
            c = i % 2

            user = models.User(
                login=f'user{i}',
                password=await get_password_hash(f'password{i}'),
                last_name=last_name[c],
                first_name=first_name[c]
            )
            session.add(user)

            try:
                await session.flush()
            except Exception:
                return False

            for tag_name in tags_names:
                tag = models.Tag(
                    name=tag_name,
                    user_id=user.id
                )
                session.add(tag)
                try:
                    await session.flush()
                except Exception:
                    return False

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
                try:
                    await session.flush()
                except Exception:
                    return False

                for tag_id in _task['tags']:
                    tag_task = models.TaskTag(
                        task_id=task.id,
                        tag_id=tag_id
                    )
                    session.add(tag_task)
                    try:
                        await session.flush()
                    except Exception:
                        return False

        try:
            await session.commit()
        except Exception:
            return False

    return True
