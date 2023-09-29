"""
Модуль схем аккаунта.
"""
from pydantic import Field

from app import db
from app.domain.schemas import APIBase


class UserLoginData(APIBase):
    login: str = Field(max_length=db.consts.MAX_LEN_USER_LOGIN)
    password: str = Field(min_length=db.consts.MIN_LEN_USER_PASSWORD, max_length=db.consts.MAX_LEN_USER_PASSWORD)


class User(APIBase):
    id: int

    login: str

    last_name: str
    first_name: str


class UserNew(APIBase):
    login: str
    password: str


class Token(APIBase):
    token: str
    type: str
