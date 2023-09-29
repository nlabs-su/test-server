from litestar import Router

from app.domain import urls
from app.domain import users, tasks, tags


def create_router() -> Router:
    return Router(
        path=urls.BASE_API_PATH,
        route_handlers=[
            users.controllers.UserController,
            tags.controllers.TagController,
            tasks.controllers.TaskController
        ]
    )
