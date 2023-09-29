"""
Модуль констант для полей БД.
"""
import re


MAX_LEN_ID: int = 2147483647

MAX_LEN_USER_LOGIN: int = 25
USER_LOGIN_REGEX: re.Pattern = re.compile(r'^[a-z0-9]{3,15}$')

MIN_LEN_USER_PASSWORD: int = 6
MAX_LEN_USER_PASSWORD: int = 30
MAX_LEN_USER_PASSWORD_HASH: int = 102

MIN_LEN_USER_LAST_NAME: int = 40
MAX_LEN_USER_FIRST_NAME: int = 40

MAX_LEN_TAG_NAME: int = 20

MAX_LEN_TASK_NAME: int = 50
MAX_LEN_TASK_DESCRIPTION: int = 500
