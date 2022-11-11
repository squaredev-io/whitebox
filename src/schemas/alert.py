from datetime import datetime
import enum
from typing import Any, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase

class AlertStatus(str, enum.Enum):
    open = "open"
    closed = "closed"

class AlertSeverity(str, enum.Enum):
    low = "low"
    mid = "mid"
    high = "high"


class AlertBase(BaseModel):
    model_monitor_id: str
    status: AlertStatus
    severity: AlertSeverity
    timestamp: Union[str, datetime]
    description: str


class Alert(AlertBase, ItemBase):
    pass

class AlertCreateDto(AlertBase):
    pass
