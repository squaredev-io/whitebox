from fastapi.encoders import jsonable_encoder
from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.PerformanceMetric import PerformanceMetric as PerformanceMetricEntity
from src.schemas.performanceMetric import PerformanceMetric, PerformanceMetricCreate


class CRUD(CRUDBase[PerformanceMetric, PerformanceMetricCreate, Any]):
    def get_model_performance_metrics(
        self, db: Session, *, model_id: int
    ) -> List[PerformanceMetric]:
        return (
            db.query(self.model)
            .filter(PerformanceMetricEntity.model_id == model_id)
            .all()
        )

performance_metrics = CRUD(PerformanceMetricEntity)
