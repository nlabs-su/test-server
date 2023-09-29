"""
Модуль получения сессии БД.
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.lib.sqlalchemy import engine


Session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    future=True,
    bind=engine,
    class_=AsyncSession
)
