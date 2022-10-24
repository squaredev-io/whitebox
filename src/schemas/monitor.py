from typing import Any, Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class MonitorBase(BaseModel):
    model_id: str
    name: str
    metric: Any
    threshold: Union[int, float]


class Monitor(MonitorBase, ItemBase):
    pass
