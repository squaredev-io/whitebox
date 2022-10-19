from typing import Optional
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class UserBase(BaseModel):
    name: str


class UserInDb(UserBase, ItemInDbBase):
    pass


# class UserCreate(BaseModel):
#     ext_id: str
#     name: str


# class UserUpdate(BaseModel):
#     name: Optional[str]
#     ext_id: Optional[str]
