from typing import Any, List
from sqlalchemy.orm import Session
from whitebox.crud.base import CRUDBase
from whitebox.entities.DriftingMetric import DriftingMetric as DriftingMetricEntity
from whitebox.schemas.driftingMetric import DriftingMetricBase


class CRUD(CRUDBase[DriftingMetricBase, Any, Any]):
    def get_model_drifting_metrics(
        self, db: Session, *, model_id: str
    ) -> List[DriftingMetricBase]:
        return db.query(self.model).filter(self.model.model_id == model_id).all()


drifting_metrics = CRUD(DriftingMetricEntity)
