from typing import Any, Optional
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class VersionBase(BaseModel):
    model_id: str
    name: str
    type: Any
    features: Any
    predictions: Any
    labels: str
    feature_importance: Any


class VersionInDb(VersionBase, ItemInDbBase):
    pass
