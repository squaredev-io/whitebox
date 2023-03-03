from typing import Dict, Optional
from pydantic import BaseModel
from whitebox.schemas.base import ItemBase
import enum


class ModelType(str, enum.Enum):
    binary = "binary"
    multi_class = "multi_class"
    regression = "regression"


class ModelBase(BaseModel):
    name: str
    description: str
    type: ModelType
    target_column: str
    granularity: str
    labels: Optional[Dict[str, int]]


class Model(ModelBase, ItemBase):
    pass


class ModelCreateDto(ModelBase):
    pass


class ModelUpdateDto(BaseModel):
    name: Optional[str]
    description: Optional[str]
    type: Optional[ModelType]
