from typing import Optional
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class ModelBase(BaseModel):
    user_id: str
    name: str


class ModelInDb(ModelBase, ItemInDbBase):
    pass
