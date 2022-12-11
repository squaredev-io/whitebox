from typing import List
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.driftingMetric import DriftingMetricBase
from whitebox.schemas.user import User
from whitebox.utils.errors import add_error_responses, errors


drifting_metrics_router = APIRouter()


@drifting_metrics_router.get(
    "/models/{model_id}/drifting-metrics",
    tags=["Drifting Metrics"],
    response_model=List[DriftingMetricBase],
    summary="Get all model's drifting metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_drifting_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):

    model = crud.models.get(db, model_id)
    if model:
        return crud.drifting_metrics.get_model_drifting_metrics(
            db=db, model_id=model_id
        )
    else:
        return errors.not_found("Model not found")
