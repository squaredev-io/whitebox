from typing import Dict, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase
from datetime import datetime


class FeatureMetrics(BaseModel):
    missing_count: Dict[str, int]
    non_missing_count: Dict[str, int]
    mean: Dict[str, float]
    minimum: Dict[str, float]
    maximum: Dict[str, float]
    sum: Dict[str, float]
    standard_deviation: Dict[str, float]
    variance: Dict[str, float]


class ModelIntegrityMetricBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    feature_metrics: FeatureMetrics


class ModelIntegrityMetric(ModelIntegrityMetricBase, ItemBase):
    pass

class ModelIntegrityMetricCreate(ModelIntegrityMetricBase):
    pass