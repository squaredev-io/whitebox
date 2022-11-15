from datetime import datetime
from typing import Dict, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class ColumnDataDriftMetrics(BaseModel):
    """One column drift metrics"""

    column_name: str
    column_type: str
    stattest_name: str
    drift_score: float
    drift_detected: bool
    threshold: float


class DataDriftTable(BaseModel):
    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]


class ConseptDriftTable(BaseModel):
    """Concept drift metrics"""


# TODO: Need to include the class of the concept drift
class DriftingMetricBase(ItemBase):
    model_id: str
    timestamp: Union[str, datetime]
    # TODO: The pipeline needs to return a DataDriftTable. If evidently does not provide it we should create it.
    # concept_drift_summary: DataDriftTable
    data_drift_summary: DataDriftTable


class DriftingMetric(DriftingMetricBase, ItemBase):
    pass
