from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.PerformanceMetric import BinaryClassificationMetrics as BinaryClassificationMetricsEntity, \
    MultiClassificationMetrics as MultiClassificationMetricsEntity
from src.schemas.performanceMetric import BinaryClassificationMetrics, MultiClassificationMetrics

class CRUD(CRUDBase[BinaryClassificationMetrics | MultiClassificationMetrics, Any, Any]):
    def get_model_performance_metrics(
        self, db: Session, *, model_id: int
    ) -> List[BinaryClassificationMetrics] | List[MultiClassificationMetrics]:
        return (
            db.query(self.model)
            .filter(self.model.model_id == model_id)
            .all()
        )

binary_classification_metrics = CRUD(BinaryClassificationMetricsEntity)
multi_classification_metrics = CRUD(MultiClassificationMetricsEntity)

