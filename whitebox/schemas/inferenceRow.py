from datetime import datetime
from typing import Any, Dict, Union, Optional
from pydantic import BaseModel
from whitebox.schemas.base import ItemBase


class InferenceRowBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    # Prediction is included into nonprocessed & processed
    nonprocessed: Dict[str, Any]
    processed: Dict[str, float]
    actual: Optional[float]


class InferenceRowCreateDto(InferenceRowBase):
    pass


class InferenceRowPreDb(InferenceRowBase):
    is_used: bool


class InferenceRow(InferenceRowPreDb, ItemBase):
    pass
