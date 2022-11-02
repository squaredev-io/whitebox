from fastapi.encoders import jsonable_encoder
from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.DriftingMetric import DriftingMetric as DriftingMetricEntity
from src.schemas.driftingMetric import DriftingMetric, DriftingMetricCreate


class CRUD(CRUDBase[DriftingMetric, DriftingMetricCreate, Any]):
    def get_model_drifting_metrics(
        self, db: Session, *, model_id: int
    ) -> List[DriftingMetric]:
        return (
            db.query(self.model)
            .filter(DriftingMetricEntity.model_id == model_id)
            .all()
        )

drifting_metrics = CRUD(DriftingMetricEntity)
