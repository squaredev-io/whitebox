from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Optional, Union

from whitebox.schemas.base import ItemBase

# TODO: Include comments of what each class represents


class BinaryClassificationMetricsBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    accuracy: float
    precision: float
    recall: float
    f1: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int


class BinaryClassificationMetrics(BinaryClassificationMetricsBase, ItemBase):
    pass


class DifferentStatistics(BaseModel):
    micro: float
    macro: float
    weighted: float


class ConfusionMatrix(BaseModel):
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int


class MultiClassificationMetricsBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    accuracy: float
    precision: DifferentStatistics
    recall: DifferentStatistics
    f1: DifferentStatistics
    confusion_matrix: Dict[str, ConfusionMatrix]


class MultiClassificationMetrics(MultiClassificationMetricsBase, ItemBase):
    pass


class MultiClassificationMetricsPipelineResult(BaseModel):
    """This class is used to store the results of the pipeline that calculates the multi classification metrics"""

    accuracy: float
    precision: DifferentStatistics
    recall: DifferentStatistics
    f1: DifferentStatistics
    confusion_matrix: Dict[str, ConfusionMatrix]


class BinaryClassificationMetricsPipelineResult(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int
