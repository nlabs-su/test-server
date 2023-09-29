"""
Модуль констант URL's.
"""
OPENAPI_SCHEMA = "/schema"

BASE_API_PATH = "/api"

USER_CREATE = "/users"
USER_LOGIN = "/user/login"
USER_PROFILE = "/user/me"

TAGS_CREATE = "/tags"
TAGS_READ = "/tags"
TAGS_UPDATE = "/tags/{id:int}"
TAGS_DELETE = "/tags/{id:int}"

TASKS_CREATE = "/tasks"
TASKS_READ = "/tasks"
TASKS_READ_BY_ID = "/tasks/{id:int}"
TASKS_TYPES_READ = "/tasks/types"
TASKS_UPDATE = "/tasks/{id:int}"
TASKS_DELETE = "/tasks/{id:int}"

TASK_TYPES = "/task-types"
