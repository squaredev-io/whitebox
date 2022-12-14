from typing import Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class UserBase(BaseModel):
    username: str


class User(UserBase, ItemBase):
    pass


class UserCreateDto(UserBase):
    api_key: str
