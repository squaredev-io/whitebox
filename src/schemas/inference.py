from datetime import datetime
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase
import enum


class InferenceBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    inference: Dict[str, Any]


class Inference(InferenceBase, ItemBase):
    pass


class InferenceCreate(InferenceBase):
    pass
