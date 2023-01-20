from pydantic import BaseModel
from whitebox.schemas.base import ItemBase
from typing import Dict, Any


class DatasetRowBase(BaseModel):
    model_id: str
    # Data before any processing
    nonprocessed: Dict[str, Any]
    # Before model entry
    processed: Dict[str, float]


class DatasetRow(DatasetRowBase, ItemBase):
    pass


class DatasetRowCreate(DatasetRowBase):
    pass
