from typing import Any, Dict
from pydantic import BaseModel
from src.schemas.base import ItemBase


class ModelIntegrityMetricBase(BaseModel):
    model_id: str
    missing_values: float
    feature_metrics: Dict[str, Any]


class ModelIntegrityMetric(ModelIntegrityMetricBase, ItemBase):
    pass


class ModelIntegrityMetricCreate(ModelIntegrityMetricBase):
    pass
