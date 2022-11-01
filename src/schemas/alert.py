from datetime import datetime
from typing import Any, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class AlertBase(BaseModel):
    model_monitor_id: str
    status: Any
    severity: Any
    timestamp: Union[str, datetime]
    description: str


class Alert(AlertBase, ItemBase):
    pass

class Alert(AlertBase):
    pass
