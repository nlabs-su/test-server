"""
Модуль модели пользователя.
"""
import sqlalchemy as sa
import sqlalchemy.orm

from .. import consts
from ... import db


class User(db.base.Base):
    """Модель таблицы аккаунтов.

    :id: Уникальный внутренний идентификатор таблицы.

    :login: Логин.
    :password: Пароль.

    :last_name: Фамилия.
    :first_name: Имя.
    """
    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, nullable=False)

    login: sa.orm.Mapped[str] = sa.orm.mapped_column(
        sa.String(consts.MAX_LEN_USER_LOGIN), nullable=False, unique=True
    )
    password: sa.orm.Mapped[str] = sa.orm.mapped_column(sa.String(consts.MAX_LEN_USER_PASSWORD_HASH), nullable=False)

    last_name: sa.orm.Mapped[str] = sa.orm.mapped_column(sa.String(consts.MIN_LEN_USER_LAST_NAME), nullable=False)
    first_name: sa.orm.Mapped[str] = sa.orm.mapped_column(sa.String(consts.MAX_LEN_USER_FIRST_NAME), nullable=False)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def __repr__(self):
        return f'{self.last_name} {self.first_name}'
