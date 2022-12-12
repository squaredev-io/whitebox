from typing import Dict, Optional
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
    name: str
    description: str
    type: ModelType

    """Inference row metadata"""

    # TODO do we need this?
    features: Dict[str, FeatureTypes]
    labels: Dict[str, int]

    prediction: str
    probability: str


class Model(ModelBase, ItemBase):
    pass


class ModelCreateDto(ModelBase):
    pass


class ModelUpdateDto(BaseModel):
    name: Optional[str]
    description: Optional[str]
    type: Optional[ModelType]
