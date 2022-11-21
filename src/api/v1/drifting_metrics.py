from typing import List, Union
from fastapi import APIRouter, Depends, status, Header
from src.crud.drifting_metrics import drifting_metrics
from src.crud.models import models
from src.crud.users import users
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.driftingMetric import DriftingMetricBase
from src.utils.errors import add_error_responses, errors


drifting_metrics_router = APIRouter()


@drifting_metrics_router.get(
    "/models/{model_id}/drifting_metrics",
    tags=["Drifting Metrics"],
    response_model=List[DriftingMetricBase],
    summary="Get all model's drifting metrics",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_drifting_metrics(
    model_id: str,
    db: Session = Depends(get_db),
    api_key: Union[str, None] = Header(default=None),
):
    authenticated = users.match_api_key(db, api_key=api_key)
    if not authenticated:
        return errors.unauthorized()

    model = models.get(db, model_id)
    if model:
        return drifting_metrics.get_model_drifting_metrics(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")
