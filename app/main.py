from typing import Any

import uvicorn
from litestar import Litestar
from litestar.di import Provide

from app import db
from app.lib import (
    openapi, settings, cors
)
from app.domain import security, create_router
from app.domain import exceptions


async def on_startup() -> None:
    await db.init_db()


def create_app(**kwargs: Any) -> Litestar:
    kwargs.setdefault("debug", settings.app.DEBUG)

    dependencies = {
        "current_user": Provide(security.provide_user)
    }

    return Litestar(
        openapi_config=openapi.config,
        on_startup=[on_startup],
        on_app_init=[security.auth.on_app_init],
        route_handlers=[create_router()],
        cors_config=cors.cors_config,
        dependencies=dependencies,
        exception_handlers={exceptions.APIError: exceptions.api_error_handler},
        **kwargs
    )


app = create_app()

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    FORMAT_LOGS = '%(levelname)-10s | %(asctime)-15s - %(message)s'

    log_config["formatters"]["access"]["fmt"] = FORMAT_LOGS
    log_config["formatters"]["default"]["fmt"] = FORMAT_LOGS

    uvicorn.run(
        app,
        host=settings.server.HOST,
        log_level=settings.server.LOG_LEVEL,
        port=settings.server.PORT,
        reload=settings.server.RELOAD,
        timeout_keep_alive=settings.server.KEEPALIVE,
        log_config=log_config
    )
