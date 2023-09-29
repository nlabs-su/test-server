"""
Модуль глобальной конфигурации.
"""
import datetime
from functools import lru_cache
from typing import Literal

from pydantic import ValidationError
from pydantic_settings import BaseSettings
from pydantic.functional_validators import field_validator


class BaseEnvSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppSettings(BaseEnvSettings):
    """Общие настройки приложения.

    Аттрибуты:
    ----------
    NAME: str
        Название проекта.
    DEBUG : bool
        Если `True`, то `Litestar` запустится с режимом дебага.
    ENVIRONMENT : str
        "dev", "prod", etc.
    LOG_LEVEL : str
        Stdlib уровень логов, "DEBUG", "INFO", etc.
    SECRET_KEY: str
        Секретный ключ.

    AUTH_JWT_ALGORITHM: Literal["HS256", "HS384", "HS512"]
        Алгоритм кодировки токена авторизации.

    APP_AUTH_TOKEN_EXPIRES_MINUTES: int
        Время действия token.

    """
    class Config:
        env_prefix = "APP_"
        case_sensitive = True

    NAME: str = "Test"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "abc123"

    AUTH_JWT_ALGORITHM: str = Literal["HS256", "HS384", "HS512"]

    AUTH_TOKEN_EXPIRES_MINUTES: int


class OpenAPISettings(BaseEnvSettings):
    """Конфигурация OpenAPI

    Префикс всех переменных окружений начинается с `OPENAPI_`, например, `OPENAPI_TITLE`.

    Аттрибуты:
    ----------
    TITLE : str
        Название проекта OpenAPI.
    VERSION : str
        Версия проекта OpenAPI.
    """

    class Config:
        env_prefix = "OPENAPI_"
        case_sensitive = True

    TITLE: str | None = "Test"
    VERSION: str = "0.1.0"


class DatabaseSettings(BaseEnvSettings):
    """Конфигурация базы данных.

    Префикс всех переменных окружений начинается с `DB_`, например, `DB_ECHO`.

    Аттрибуты:
    ----------
    PATH: str
        Путь до базы данных sqlite.
    ECHO : bool
        Включает логи движка SQLAlchemy.
    """

    class Config:
        env_prefix = "DB_"
        case_sensitive = True

    PATH: str
    ECHO: bool = False


class ServerSettings(BaseEnvSettings):
    """Конфигурация сервера.

    Префикс всех переменных окружений начинается с `SERVER_`, например, `SERVER_HOST`.

    Аттрибуты:
    ----------
    HOST : str
        Адрес сервера.
    PORT: int
        Порт сервера.
    KEEPALIVE: int
        ...
    LOG_LEVEL: str
        Уровень логирования.
    RELOAD: bool:
        ...
    TIMEOUT: int
        ...
    """
    class Config:
        env_prefix = "SERVER_"
        case_sensitive = True

    HOST: str = "localhost"
    PORT: int = 5000
    KEEPALIVE: int = 65
    LOG_LEVEL: str = "info"
    RELOAD: bool = False
    TIMEOUT: int = 65


@lru_cache
def load_settings() -> (
    tuple[
        AppSettings,
        DatabaseSettings,
        OpenAPISettings,
        ServerSettings
    ]
):
    try:
        app: AppSettings = AppSettings()
        db: DatabaseSettings = DatabaseSettings()
        openapi: OpenAPISettings = OpenAPISettings()
        server: ServerSettings = ServerSettings()

    except ValidationError as e:
        print("Could not load settings. %s", e)  # noqa: T201
        raise e from e
    return (
        app,
        db,
        openapi,
        server
    )


(
    app,
    db,
    openapi,
    server
) = load_settings()
