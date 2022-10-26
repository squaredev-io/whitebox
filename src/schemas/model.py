from typing import Any, Optional
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


class Model(ModelBase, ItemBase):
    pass


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str]
    type: Optional[ModelType]
