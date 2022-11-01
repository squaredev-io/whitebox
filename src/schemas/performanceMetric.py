from pydantic import BaseModel
from src.schemas.base import ItemBase


class PerformanceMetricBase(BaseModel):
    model_id: str
    precision: float
    recall: float
    f1: float
    accuracy: float
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int


class PerformanceMetric(PerformanceMetricBase, ItemBase):
    pass


class PerformanceMetricCreate(PerformanceMetricBase):
    pass
