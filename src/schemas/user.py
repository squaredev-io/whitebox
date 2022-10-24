from typing import Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase, ItemBase):
    pass


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: Optional[str]
    email: Optional[str]
    password: Union[str, None] = None
