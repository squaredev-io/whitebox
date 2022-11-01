from pydantic import BaseModel
from src.schemas.base import ItemBase


class DatasetBase(BaseModel):
    user_id: str
    name: str


class Dataset(DatasetBase, ItemBase):
    pass


class DatasetCreate(DatasetBase):
    pass
