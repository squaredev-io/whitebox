from fastapi.encoders import jsonable_encoder
from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.ModelIntegrityMetric import ModelIntegrityMetric as ModelIntegrityMetricEntity
from src.schemas.modelIntegrityMetric import ModelIntegrityMetricBase


class CRUD(CRUDBase[ModelIntegrityMetricBase, Any, Any]):
    def get_model_model_integrity_metrics(
        self, db: Session, *, model_id: int
    ) -> List[ModelIntegrityMetricBase]:
        return (
            db.query(self.model)
            .filter(ModelIntegrityMetricEntity.model_id == model_id)
            .all()
        )

model_integrity_metrics = CRUD(ModelIntegrityMetricEntity)
