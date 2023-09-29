"""
Модуль конфигурации CORS.
"""
from litestar.config.cors import CORSConfig


cors_config = CORSConfig(allow_origins=['*'], allow_credentials=True)
