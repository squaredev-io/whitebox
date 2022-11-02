from typing import List
from fastapi import APIRouter, Depends, status
from src.crud.performance_metrics import performance_metrics
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.performanceMetric import PerformanceMetric
from src.utils.errors import errors


performance_metrics_router = APIRouter()


@performance_metrics_router.get(
    "/models/{model_id}/performance_metrics",
    tags=["Performance Metrics"],
    response_model=List[PerformanceMetric],
    summary="Get all model's performance metrics",
    status_code=status.HTTP_200_OK,
)
async def get_all_models_performance_metrics(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db, model_id)
    if model:
        return performance_metrics.get_model_performance_metrics(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")


@performance_metrics_router.get(
    "/performance_metrics/{performance_metric_id}",
    tags=["Performance Metrics"],
    response_model=PerformanceMetric,
    status_code=status.HTTP_200_OK,
    summary="Get performance metric by id",
)
async def get_performance_metric(performance_metric_id: str, db: Session = Depends(get_db)):
    performance_metric = performance_metrics.get(db=db, _id=performance_metric_id)
    if not performance_metric:
        return errors.not_found("Performance metric not found")

    return performance_metric
