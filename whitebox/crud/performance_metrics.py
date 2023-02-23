from typing import Any, List, Union
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from whitebox.crud.base import CRUDBase
from whitebox.entities.PerformanceMetric import (
    BinaryClassificationMetrics as BinaryClassificationMetricsEntity,
    MultiClassificationMetrics as MultiClassificationMetricsEntity,
    RegressionMetrics as RegressionMetricsEntity,
)
from whitebox.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
    RegressionMetrics,
)


class CRUD(
    CRUDBase[Union[BinaryClassificationMetrics, MultiClassificationMetrics], Any, Any]
):
    def get_performance_metrics_by_model(
        self, db: Session, *, model_id: int
    ) -> Union[
        List[BinaryClassificationMetrics],
        List[MultiClassificationMetrics],
        List[RegressionMetrics],
    ]:
        return (
            db.query(self.model)
            .filter(self.model.model_id == model_id)
            .order_by(asc("timestamp"))
            .all()
        )

    def get_latest_report_by_model(
        self, db: Session, *, model_id: int
    ) -> Union[
        BinaryClassificationMetrics, MultiClassificationMetrics, RegressionMetrics
    ]:
        return (
            db.query(self.model)
            .filter(self.model.model_id == model_id)
            .order_by(desc("created_at"))
            .first()
        )


binary_classification_metrics = CRUD(BinaryClassificationMetricsEntity)
multi_classification_metrics = CRUD(MultiClassificationMetricsEntity)
regression_metrics = CRUD(RegressionMetricsEntity)
