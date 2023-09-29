"""
Базовый модуль схем.
"""
from pydantic import BaseModel


class APIBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


class Code(APIBase):
    code: str
