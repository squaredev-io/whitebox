from typing import List
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.modelIntegrityMetric import ModelIntegrityMetric
from whitebox.schemas.user import User
from whitebox.utils.errors import add_error_responses, errors


model_integrity_metrics_router = APIRouter()


@model_integrity_metrics_router.get(
    "/models/{model_id}/model-integrity-metrics",
    tags=["Model Integrity Metrics"],
    response_model=List[ModelIntegrityMetric],
    summary="Get all model's model integrity metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_model_integrity_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):

    model = crud.models.get(db, model_id)
    if model:
        return crud.model_integrity_metrics.get_model_model_integrity_metrics(
            db=db, model_id=model_id
        )
    else:
        return errors.not_found("Model not found")
