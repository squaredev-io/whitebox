from typing import List, Union
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.alert import Alert
from whitebox.schemas.user import User
from whitebox.utils.errors import add_error_responses, errors


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
    """
    Fetches alerts from the databse.
    \n If a model id is provided, only the alerts for the specific model will be fetched.
    \n If a model id is not provided then all alerts from the database will be fetched.
    """

    if model_id:
        model = crud.models.get(db, model_id)
        if model:
            return crud.alerts.get_model_alerts_by_model(db=db, model_id=model_id)
        else:
            return errors.not_found("Model not found")
    else:
        return crud.alerts.get_all(db=db)
