from pydantic import BaseModel
from typing import Dict
from src.schemas.base import ItemBase

# TODO: Include comments of what each class represents


class BinaryClassificationMetrics(BaseModel):
    model_id: str
    timestamp: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int


class DifferentStatistics(BaseModel):
    micro: float
    macro: float
    weighted: float


class ConfusionMatrix(BaseModel):
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int


class MultiClassificationMetrics(BaseModel):
    model_id: str
    timestamp: str
    accuracy: float
    precision: DifferentStatistics
    recall: DifferentStatistics
    f1: DifferentStatistics
    confusion_matrix: Dict[str, ConfusionMatrix]
