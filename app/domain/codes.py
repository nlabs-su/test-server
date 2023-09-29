"""
Модуль ответов сервера на запросы.
"""
BAD_REQUEST = 'BAD_REQUEST'
"""Используется в случаях, когда произошла ошибка связанная с БД."""

NOT_FOUND = 'NOT_FOUND'
"""Искомая сущность не найдена в БД."""

TAG_NOT_FOUND = 'TAG_NOT_FOUND'
"""Тег не найден."""

TAG_ALREADY_EXISTS = 'TAG_ALREADY_EXISTS'
"""Тег уже существует."""

TASK_ALREADY_EXISTS = 'TASK_ALREADY_EXISTS'
"""Задача уже существует."""

SUCCESS = 'SUCCESS'
"""Запрос успешно обработан."""

AUTHORIZATION_REQUIRED = 'AUTHORIZATION_REQUIRED'
"""Для доступа к эндпоинту необходима авторизация."""

ALREADY_AUTHORIZED = 'ALREADY_AUTHORIZED'
"""Если аккаунт авторизован и повторно пытается авторизоваться, то возвращается данный код."""

INVALID_AUTHORIZATION = 'INVALID_AUTHORIZATION'
"""При авторизации сотрудник вводит не правильный логин или пароль"""

TOKEN_EXPIRED = 'TOKEN_EXPIRED'
"""Срок действия токена истек"""

TOKEN_INVALID = 'TOKEN_INVALID'
"""Токен невалидный"""
