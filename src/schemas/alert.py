import datetime
from typing import Any
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class AlertBase(BaseModel):
    monitor_id: str
    status: Any
    severity: Any
    timestamp: datetime.datetime
    description: str


class AlertInDb(AlertBase, ItemInDbBase):
    pass
