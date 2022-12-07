from pydantic import BaseModel
import enum
from src.schemas.base import ItemBase


class MonitorStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class MonitorMetrics(str, enum.Enum):
    accuracy = "accuracy"
    precision = "precision"
    recall = "recall"
    f1 = "f1"
    data_drift = "data_drift"
    concept_drift = "concept_drift"
    missing_values_count = "missing_values_count"


class AlertSeverity(str, enum.Enum):
    low = "low"
    mid = "mid"
    high = "high"


class ModelMonitorBase(BaseModel):
    model_id: str
    name: str
    status: MonitorStatus
    metric: MonitorMetrics
    threshold: float
    severity: AlertSeverity
    email: str


class ModelMonitor(ModelMonitorBase, ItemBase):
    pass


class ModelMonitorCreateDto(ModelMonitorBase):
    pass
