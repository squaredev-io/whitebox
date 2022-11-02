from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from src.schemas.base import ItemBase
import enum


class ModelType(str, enum.Enum):
    binary = "binary"
    multi_class = "multi_class"


class FeatureTypes(str, enum.Enum):
    categorical = "categorical"
    boolean = "boolean"
    string = "string"
    datetime = "datetime"
    numerical = "numerical"


class ModelBase(BaseModel):
    user_id: str
    name: str
    description: str
    type: ModelType
    features: Dict[str, FeatureTypes]
    labels: Optional[List[str]]


class Model(ModelBase, ItemBase):
    pass


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    type: Optional[ModelType]
