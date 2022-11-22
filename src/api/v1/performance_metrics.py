from typing import List, Union
from fastapi import APIRouter, Depends, status, Header
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
)
from src.utils.errors import add_error_responses, errors


performance_metrics_router = APIRouter()


@performance_metrics_router.get(
    "/models/{model_id}/performance-metrics",
    tags=["Performance Metrics"],
    response_model=List[BinaryClassificationMetrics] | List[MultiClassificationMetrics],
    summary="Get all model's performance metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_performance_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    api_key: Union[str, None] = Header(default=None),
):
    authenticated = crud.users.authenticate(db, api_key=api_key)
    if not authenticated:
        return errors.unauthorized()

    model = crud.models.get(db, model_id)
    if model:
        if model.__dict__["type"] == "binary":
            return crud.binary_classification_metrics.get_model_performance_metrics(
                db=db, model_id=model_id
            )
        else:
            return crud.multi_classification_metrics.get_model_performance_metrics(
                db=db, model_id=model_id
            )
    else:
        return errors.not_found("Model not found")
