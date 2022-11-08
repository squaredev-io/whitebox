from pydantic import BaseModel
from src.schemas.base import ItemBase
from typing import Dict, Any


class DatasetBase(BaseModel):
    user_id: str
    name: str
    # Should be same in both processed and non processed
    target: str

class Dataset(DatasetBase, ItemBase):
    pass


class DatasetCreateDto(DatasetBase):
    pass


class DatasetRowBase(BaseModel):
    dataset_id: str
    # Data before any processing
    nonprocessed: Dict[str, Any]
    # Before model entry
    processed: Dict[str, float]

class DatasetRow(DatasetRowBase, ItemBase):
    pass

class DatasetRowCreate(DatasetRowBase):
    pass