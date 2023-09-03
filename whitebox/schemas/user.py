from pydantic import BaseModel
from whitebox.schemas.base import ItemBase


class UserBase(BaseModel):
    username: str


class User(UserBase, ItemBase):
    pass


class UserCreateDto(UserBase):
    api_key: str
