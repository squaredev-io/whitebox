from typing import List, Union
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
    RegressionMetrics,
)
from whitebox.schemas.user import User
from whitebox.schemas.model import ModelType
from whitebox.utils.errors import add_error_responses, errors


performance_metrics_router = APIRouter()


@performance_metrics_router.get(
    "/performance-metrics",
    tags=["Performance Metrics"],
    response_model=Union[
        List[BinaryClassificationMetrics],
        List[MultiClassificationMetrics],
        List[RegressionMetrics],
    ],
    summary="Get all model's performance metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_performance_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """Fetches the performance metrics of a specific model. A model id is required."""

    model = crud.models.get(db, model_id)
    if model:
        if vars(model)["type"] == ModelType.binary:
            return crud.binary_classification_metrics.get_by_model(
                db=db, model_id=model_id
            )
        elif vars(model)["type"] == ModelType.multi_class:
            return crud.multi_classification_metrics.get_by_model(
                db=db, model_id=model_id
            )
        elif vars(model)["type"] == ModelType.regression:
            return crud.regression_metrics.get_by_model(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")
