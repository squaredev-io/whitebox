from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Union
from whitebox.schemas.base import ItemBase

# TODO: Include comments of what each class represents


class BinaryClassificationMetricsPipelineResult(BaseModel):
    """This class is used to store the results of the pipeline that calculates the binary classification metrics"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int


class BinaryClassificationMetricsBase(BinaryClassificationMetricsPipelineResult):
    model_id: str
    timestamp: Union[str, datetime]


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


class MultiClassificationMetricsPipelineResult(BaseModel):
    """This class is used to store the results of the pipeline that calculates the multi classification metrics"""

    accuracy: float
    precision: DifferentStatistics
    recall: DifferentStatistics
    f1: DifferentStatistics
    confusion_matrix: Dict[str, ConfusionMatrix]


class MultiClassificationMetricsBase(MultiClassificationMetricsPipelineResult):
    model_id: str
    timestamp: Union[str, datetime]


class MultiClassificationMetrics(MultiClassificationMetricsBase, ItemBase):
    pass


class RegressionMetricsPipelineResult(BaseModel):
    """This class is used to store the results of the pipeline that calculates the regression metrics"""

    r_square: float
    mean_squared_error: float
    mean_absolute_error: float


class RegressionMetricsBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]


class RegressionMetrics(RegressionMetricsBase, ItemBase):
    pass
