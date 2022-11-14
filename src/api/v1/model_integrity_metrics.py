from typing import List
from fastapi import APIRouter, Depends, status
from src.crud.model_integrity_metrics import model_integrity_metrics
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.modelIntegrityMetric import ModelIntegrityMetric
from src.utils.errors import add_error_responses, errors


model_integrity_metrics_router = APIRouter()


@model_integrity_metrics_router.get(
    "/models/{model_id}/model_integrity_metrics",
    tags=["Model Integrity Metrics"],
    response_model=List[ModelIntegrityMetric],
    summary="Get all model's model integrity metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_all_models_model_integrity_metrics(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db, model_id)
    if model:
        return model_integrity_metrics.get_model_model_integrity_metrics(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")


@model_integrity_metrics_router.get(
    "/model_integrity_metrics/{model_integrity_metric_id}",
    tags=["Model Integrity Metrics"],
    response_model=ModelIntegrityMetric,
    summary="Get model integrity metric by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_model_integrity_metric(model_integrity_metric_id: str, db: Session = Depends(get_db)):
    model_integrity_metric = model_integrity_metrics.get(db=db, _id=model_integrity_metric_id)
    if not model_integrity_metric:
        return errors.not_found("Model integrity metric not found")

    return model_integrity_metric
