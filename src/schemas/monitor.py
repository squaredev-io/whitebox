from typing import Any, Optional, Union
from pydantic import BaseModel
from src.schemas.base import ItemInDbBase


class MonitorBase(BaseModel):
    version_id: str
    name: str
    metric: Any
    threshold: Union[int, float]


class MonitorInDb(MonitorBase, ItemInDbBase):
    pass
