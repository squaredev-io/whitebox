from typing import Any, Optional
from pydantic import BaseModel
from src.schemas.base import ItemBase


class ModelBase(BaseModel):
    project_id: str
    name: str
    type: Any
    features: Any
    predictions: Any
    labels: str
    feature_importance: Any


class Model(ModelBase, ItemBase):
    pass
