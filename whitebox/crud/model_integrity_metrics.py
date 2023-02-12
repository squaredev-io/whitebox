from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import asc
from whitebox.crud.base import CRUDBase
from whitebox.entities.ModelIntegrityMetric import (
    ModelIntegrityMetric as ModelIntegrityMetricEntity,
)
from whitebox.schemas.modelIntegrityMetric import (
    ModelIntegrityMetricCreate,
    ModelIntegrityMetric,
)


class CRUD(CRUDBase[ModelIntegrityMetric, ModelIntegrityMetricCreate, Any]):
    def get_model_integrity_metrics_by_model(
        self, db: Session, *, model_id: str
    ) -> List[ModelIntegrityMetric]:
        return (
            db.query(self.model)
            .filter(ModelIntegrityMetricEntity.model_id == model_id)
            .order_by(asc("timestamp"))
            .all()
        )


model_integrity_metrics = CRUD(ModelIntegrityMetricEntity)
