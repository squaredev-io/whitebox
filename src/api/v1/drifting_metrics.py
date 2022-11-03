from typing import List
from fastapi import APIRouter, Depends, status
from src.crud.drifting_metrics import drifting_metrics
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.driftingMetric import DriftingMetricBase
from src.utils.errors import errors


drifting_metrics_router = APIRouter()


@drifting_metrics_router.get(
    "/models/{model_id}/drifting_metrics",
    tags=["Drifting Metrics"],
    response_model=List[DriftingMetricBase],
    summary="Get all model's drifting metrics",
    status_code=status.HTTP_200_OK,
)
async def get_all_models_drifting_metrics(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db, model_id)
    if model:
        return drifting_metrics.get_model_drifting_metrics(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")


@drifting_metrics_router.get(
    "/drifting_metrics/{drifting_metric_id}",
    tags=["Drifting Metrics"],
    response_model=DriftingMetricBase,
    status_code=status.HTTP_200_OK,
    summary="Get drifting metric by id",
)
async def get_drifting_metric(drifting_metric_id: str, db: Session = Depends(get_db)):
    drifting_metric = drifting_metrics.get(db=db, _id=drifting_metric_id)
    if not drifting_metric:
        return errors.not_found("Drifting metric not found")

    return drifting_metric
