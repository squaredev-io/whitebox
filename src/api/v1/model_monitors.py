from typing import List, Union
from src.middleware.auth import authenticate_user
from src.schemas.modelMonitor import ModelMonitor, ModelMonitorCreateDto
from fastapi import APIRouter, Depends, status
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.user import User
from src.utils.errors import add_error_responses, errors


model_monitors_router = APIRouter()


@model_monitors_router.post(
    "/model-monitors",
    tags=["Model Monitors"],
    response_model=ModelMonitor,
    summary="Create a model monitor",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 409]),
)
async def create_model_monitor(
    body: ModelMonitorCreateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> ModelMonitor:

    new_model_monitor = crud.model_monitors.create(db=db, obj_in=body)
    return new_model_monitor


@model_monitors_router.get(
    "/model-monitors",
    tags=["Model Monitors"],
    response_model=List[ModelMonitor],
    summary="Get all model's model monitors",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_model_monitors(
    model_id: Union[str, None] = None,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    if model_id:
        model = crud.models.get(db, model_id)
        if model:
            return crud.model_monitors.get_model_monitors_by_model(
                db=db, model_id=model_id
            )
        else:
            return errors.not_found("Model not found")
    else:
        return crud.model_monitors.get_all(db=db)
