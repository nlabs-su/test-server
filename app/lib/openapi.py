"""
Модуль конфигурации OpenAPI.
"""
from litestar.openapi.config import OpenAPIConfig

from app.lib import settings
from app.domain.security import auth


config = OpenAPIConfig(
    title=settings.openapi.TITLE or settings.app.NAME,
    version=settings.openapi.VERSION,
    components=[auth.openapi_components],
    security=[auth.security_requirement],
    use_handler_docstrings=True,
)
