"""
Модуль моделей задач.
"""
import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm

from ... import db


if TYPE_CHECKING:
    from .tag import Tag
    from .user import User


class Type(IntEnum):
    """Список констант для типа задачи"""
    ADDED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

    @classmethod
    def to_dict(cls):
        return {e.name: e.value for e in cls}


class Task(db.base.Base):
    """Модель таблицы задач.

    :id: Уникальный внутренний идентификатор таблицы.

    :name: Название задачи.
    :description: Описание задачи.

    :date: Дата задачи.

    :type: Тип задачи.

    :account_id: Идентификатор пользователя.

    :timestamp: Дата и время создания.
    """
    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, nullable=False)

    name: sa.orm.Mapped[str] = sa.orm.mapped_column(sa.String)
    description: sa.orm.Mapped[str | None] = sa.orm.mapped_column(sa.String, nullable=True)

    date: sa.orm.Mapped[datetime.date] = sa.orm.mapped_column(sa.Date, nullable=False)

    type: sa.orm.Mapped[Type] = sa.orm.mapped_column(sa.Enum(Type), nullable=False)

    user_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    timestamp: sa.orm.Mapped[datetime.datetime] = sa.orm.mapped_column(nullable=False, default=sa.func.now())

    user: sa.orm.Mapped["User"] = sa.orm.relationship('User', lazy='noload')

    tags: sa.orm.Mapped[list["Tag"]] = sa.orm.relationship(
        'Tag',
        lazy='noload',
        uselist=True,
        secondary="join(TaskTag, Tag, TaskTag.tag_id == Tag.id)",
        secondaryjoin="Tag.id == TaskTag.tag_id",
        primaryjoin='''and_(
                    TaskTag.task_id == Task.id,
                    Tag.id == TaskTag.tag_id
                )''',
        order_by='Tag.id'
    )


class TaskTag(db.base.Base):
    """Модель таблицы тегов задач.

    :task_id: Идентификатор задачи.
    :tag_id: Идентификатор тега.
    """
    task_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('task.id'), primary_key=True, nullable=False)
    tag_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('tag.id'), primary_key=True, nullable=False)
