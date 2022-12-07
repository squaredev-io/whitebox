from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.DriftingMetric import DriftingMetric as DriftingMetricEntity
from src.schemas.driftingMetric import DriftingMetric


class CRUD(CRUDBase[DriftingMetric, Any, Any]):
    def get_drifting_metrics_by_model(
        self, db: Session, *, model_id: str
    ) -> List[DriftingMetric]:
        return (
            db.query(self.model).filter(DriftingMetricEntity.model_id == model_id).all()
        )


drifting_metrics = CRUD(DriftingMetricEntity)
