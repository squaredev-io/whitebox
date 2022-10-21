from typing import Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class UserBase(BaseModel):
    name: str
    email: str
    password: Union[str, None] = None


class UserInDb(UserBase, ItemInDbBase):
    pass


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: Optional[str]
    email: Optional[str]
