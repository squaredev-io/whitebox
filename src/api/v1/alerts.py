from typing import List, Union
from fastapi import APIRouter, Depends, status
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.middleware.auth import authenticate_user
from src.schemas.alert import Alert
from src.schemas.user import User
from src.utils.errors import add_error_responses, errors


alerts_router = APIRouter()


@alerts_router.get(
    "/alerts",
    tags=["Alerts"],
    response_model=List[Alert],
    summary="Get all model's alerts",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_alerts(
    model_id: Union[str, None] = None,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    if model_id:
        model = crud.models.get(db, model_id)
        if model:
            return crud.alerts.get_model_alerts_by_model(db=db, model_id=model_id)
        else:
            return errors.not_found("Model not found")
    else:
        return crud.alerts.get_all(db=db)
