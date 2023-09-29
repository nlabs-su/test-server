"""
Модуль базы данных.
"""
import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession  # noqa
from asyncpg import InvalidCatalogNameError

from app.db import (
    base, models, queries,
    consts
)
from app.db.session import Session
from app.lib.sqlalchemy import engine


async def init_db() -> None:
    """
    Инициализация таблиц базы данных.
    """
    from . import models

    try:
        async with engine.begin() as conn:
            await conn.run_sync(base.Base.metadata.create_all)
    except (sa.exc.DBAPIError, InvalidCatalogNameError):
        exit()
