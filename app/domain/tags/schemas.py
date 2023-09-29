"""
Модуль схем тегов.
"""
from pydantic import Field

from app.db import consts
from app.domain.schemas import APIBase


class Tag(APIBase):
    id: int

    name: str


class TagCreate(APIBase):
    name: str = Field(max_length=consts.MAX_LEN_TAG_NAME)


class ReadTags(APIBase):
    result: list[Tag]


class TagUpdate(APIBase):
    name: str = Field(max_length=consts.MAX_LEN_TAG_NAME)
