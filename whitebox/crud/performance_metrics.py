from typing import Any, List, Union
from sqlalchemy.orm import Session
from whitebox.crud.base import CRUDBase
from whitebox.entities.PerformanceMetric import (
    BinaryClassificationMetrics as BinaryClassificationMetricsEntity,
    MultiClassificationMetrics as MultiClassificationMetricsEntity,
)
from whitebox.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
)


class CRUD(
    CRUDBase[Union[BinaryClassificationMetrics, MultiClassificationMetrics], Any, Any]
):
    def get_model_performance_metrics(
        self, db: Session, *, model_id: int
    ) -> Union[List[BinaryClassificationMetrics], List[MultiClassificationMetrics]]:
        return db.query(self.model).filter(self.model.model_id == model_id).all()


binary_classification_metrics = CRUD(BinaryClassificationMetricsEntity)
multi_classification_metrics = CRUD(MultiClassificationMetricsEntity)
