from datetime import datetime
from typing import Any, Dict, Union, Optional, overload
from pydantic import BaseModel
from src.schemas.base import ItemBase


class InferenceRowBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    # Prediction is included into nonprocessed & processed
    nonprocessed: Dict[str, Any]
    processed: Dict[str, float]
    actual: Optional[float]


class InferenceRow(InferenceRowBase, ItemBase):
    pass


class InferenceRowCreateDto(InferenceRowBase):
    pass
