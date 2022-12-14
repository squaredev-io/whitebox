from typing import Any, List, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.crud.base import CRUDBase
from src.entities.PerformanceMetric import (
    BinaryClassificationMetrics as BinaryClassificationMetricsEntity,
    MultiClassificationMetrics as MultiClassificationMetricsEntity,
)
from src.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
)


class CRUD(
    CRUDBase[Union[BinaryClassificationMetrics, MultiClassificationMetrics], Any, Any]
):
    def get_by_model(
        self, db: Session, *, model_id: int
    ) -> Union[List[BinaryClassificationMetrics], List[MultiClassificationMetrics]]:
        return db.query(self.model).filter(self.model.model_id == model_id).all()

    def get_latest_report_by_model(
        self, db: Session, *, model_id: int
    ) -> Union[BinaryClassificationMetrics, MultiClassificationMetrics]:
        return (
            db.query(self.model)
            .filter(self.model.model_id == model_id)
            .order_by(desc("created_at"))
            .first()
        )


binary_classification_metrics = CRUD(BinaryClassificationMetricsEntity)
multi_classification_metrics = CRUD(MultiClassificationMetricsEntity)
