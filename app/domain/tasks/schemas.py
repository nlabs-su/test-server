"""
Модуль схем задач.
"""
import datetime

from pydantic import Field

from app.db import consts
from app.db.models import Type
from app.domain.schemas import APIBase


class TaskUser(APIBase):
    id: int

    login: str

    last_name: str
    first_name: str


class TaskTag(APIBase):
    id: int

    name: str


class Task(APIBase):
    id: int

    name: str
    description: str | None

    date: datetime.date

    type: Type

    timestamp: datetime.datetime

    tags: list[TaskTag]


class TaskCreate(APIBase):
    name: str = Field(max_length=consts.MAX_LEN_TASK_NAME)
    description: str | None = Field(max_length=consts.MAX_LEN_TASK_DESCRIPTION)

    date: datetime.date

    type: Type

    tags: list[int] = Field([])


class ReadTasks(APIBase):
    result: list[Task]


class TaskUpdate(APIBase):
    name: str = Field(max_length=consts.MAX_LEN_TASK_NAME)
    description: str | None = Field(max_length=consts.MAX_LEN_TASK_DESCRIPTION)

    date: datetime.date

    type: Type

    tags: list[int] = Field([])

