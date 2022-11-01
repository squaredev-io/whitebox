from typing import Any, Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class ModelMonitorBase(BaseModel):
    model_id: str
    dataset_id: str
    name: str
    metric: Any
    threshold: Union[int, float]


class ModelMonitor(ModelMonitorBase, ItemBase):
    pass

class ModelMonitorCreate(ModelMonitorBase):
    pass