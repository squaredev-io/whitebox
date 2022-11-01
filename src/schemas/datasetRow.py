from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Union
from src.schemas.base import ItemBase


class DatasetRowBase(BaseModel):
    dataset_id: str
    timestamp: Union[str, datetime]
    features: Dict[str, Any]
    raw: Dict[str, Any]
    prediction: Dict[str, Any]
    actuals: Dict[str, Any]


class DatasetRow(DatasetRowBase, ItemBase):
    pass


class DatasetRowCreate(DatasetRowBase):
    pass
