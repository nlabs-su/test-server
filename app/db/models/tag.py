"""
Модуль модели тега.
"""
import sqlalchemy as sa
import sqlalchemy.orm

from ... import db


class Tag(db.base.Base):
    """Модель таблицы тегов.

    :id: Уникальный внутренний идентификатор таблицы.

    :name: Название.

    :user_id: Идентификатор пользователя.
    """
    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, nullable=False)

    name: sa.orm.Mapped[str] = sa.orm.mapped_column(nullable=False)

    user_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
