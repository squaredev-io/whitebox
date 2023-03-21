from typing import Optional
from pydantic import BaseModel
import enum
from whitebox.schemas.base import ItemBase


class MonitorStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class MonitorMetrics(str, enum.Enum):
    # Performance metrics
    accuracy = "accuracy"
    precision = "precision"
    recall = "recall"
    f1 = "f1"
    r_square = "r_square"
    mean_squared_error = "mean_squared_error"
    mean_absolute_error = "mean_absolute_error"

    # Drifting metrics
    data_drift = "data_drift"
    concept_drift = "concept_drift"


class AlertSeverity(str, enum.Enum):
    low = "low"
    mid = "mid"
    high = "high"


class ModelMonitorBase(BaseModel):
    model_id: str
    name: str
    status: MonitorStatus
    metric: MonitorMetrics
    severity: AlertSeverity
    email: str
    feature: Optional[str]
    lower_threshold: Optional[float]


class ModelMonitor(ModelMonitorBase, ItemBase):
    pass


class ModelMonitorCreateDto(ModelMonitorBase):
    pass


class ModelMonitorUpdateDto(BaseModel):
    name: Optional[str]
    status: Optional[MonitorStatus]
    severity: Optional[AlertSeverity]
    email: Optional[str]
    lower_threshold: Optional[float]
