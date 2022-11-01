from typing import Any, Dict
from pydantic import BaseModel
from src.schemas.base import ItemBase


class FeatureMetrics(BaseModel):
    missing_count: Dict[str, int]
    non_missing_count: Dict[str, int]
    mean: Dict[str, float]
    minimun: Dict[str, float]
    maximum: Dict[str, float]
    sum: Dict[str, float]
    standard_deviation: Dict[str, float]
    variance: Dict[str, float]


class ModelIntegrityMetricBase(BaseModel):
    model_id: str
    timestamp: str
    feature_metrics: FeatureMetrics
