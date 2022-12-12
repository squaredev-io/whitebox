from datetime import datetime
from typing import Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class AlertBase(BaseModel):
    model_id: str
    model_monitor_id: str
    timestamp: Union[str, datetime]
    description: str


class Alert(AlertBase, ItemBase):
    pass


class AlertCreateDto(AlertBase):
    pass
