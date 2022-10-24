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

class ModelCreate(ModelBase):
    pass

class ModelUpdate(BaseModel):
    name: Optional[str]
    type: Optional[Any]
    features:  Optional[Any]
    predictions:  Optional[Any]
    labels: Optional[str]
    feature_importance: Optional[Any]
