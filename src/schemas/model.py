from typing import Any, Dict, Optional
from pydantic import BaseModel
from src.schemas.base import ItemBase
import enum


class ModelType(str, enum.Enum):
    binary = "binary"
    multi_class = "multi_class"


class ModelBase(BaseModel):
    user_id: str
    name: str
    type: ModelType
    features: Dict[str, Any]
    predictions: Dict[str, Any]
    labels: Dict[str, Any]


class Model(ModelBase, ItemBase):
    pass


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str]
    type: Optional[ModelType]
