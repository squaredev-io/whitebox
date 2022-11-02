from pydantic import BaseModel
from src.schemas.base import ItemBase

# TODO: Avoid using Evidently's schema and create a new one
from evidently.metrics import DataDriftTable

# TODO: Need to include the class of the concept drift
class DriftingMetricBase(BaseModel):
    model_id: str
    timestamp: str
    concept_drift_summary: float
    data_drift_summary: DataDriftTable
