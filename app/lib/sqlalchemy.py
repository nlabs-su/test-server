"""
Модуль подключения к базе данных.
"""
from sqlalchemy.ext.asyncio import create_async_engine

from app.lib import settings


engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.db.PATH}",
    echo=settings.db.ECHO,
    pool_pre_ping=True,
    future=True,
)
