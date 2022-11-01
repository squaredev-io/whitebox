from pydantic import BaseModel
from src.schemas.base import ItemBase


class DriftingMetricBase(BaseModel):
    model_id: str
    context_distance: float
    data_distance: float


class DriftingMetric(DriftingMetricBase, ItemBase):
    pass


class DriftingMetricCreate(DriftingMetricBase):
    pass
