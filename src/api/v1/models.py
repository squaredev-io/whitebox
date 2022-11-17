from typing import List, Union
from src.schemas.model import Model, ModelCreateDto, ModelUpdateDto
from fastapi import APIRouter, Depends, status, Header
from src.crud.models import models
from src.crud.users import users
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.utils import StatusCode
from src.utils.errors import add_error_responses, errors


models_router = APIRouter()


@models_router.post(
    "/models",
    tags=["Models"],
    response_model=Model,
    summary="Create model",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 409]),
)
async def create_model(
    body: ModelCreateDto,
    db: Session = Depends(get_db),
    api_key: Union[str, None] = Header(default=None),
) -> Model:
    authenticated = users.match_api_key(db, api_key=api_key)
    if not authenticated:
        return errors.unauthorized()
    if body is not None:
        body.user_id = authenticated.id
        new_model = models.create(db=db, obj_in=body)
        return new_model
    else:
        return errors.bad_request("Form should not be empty")


@models_router.get(
    "/models",
    tags=["Models"],
    response_model=List[Model],
    summary="Get all models",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_all_models(db: Session = Depends(get_db)):
    models_in_db = models.get_all(db=db)
    if not models_in_db:
        return errors.not_found("No model found in database")

    return models_in_db


@models_router.get(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model,
    summary="Get model by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_model(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")

    return model


@models_router.put(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model,
    summary="Update model",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([400, 404]),
)
async def update_model(
    model_id: str,
    body: ModelUpdateDto,
    db: Session = Depends(get_db),
) -> Model:
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")
    if body is not None:
        return models.update(db=db, db_obj=model, obj_in=body)
    else:
        return errors.bad_request("Form should not be empty")


@models_router.delete(
    "/models/{model_id}",
    tags=["Models"],
    response_model=StatusCode,
    summary="Delete user",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def delete_model(
    model_id: str,
    db: Session = Depends(get_db),
) -> StatusCode:
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")

    models.remove(db=db, _id=model_id)
    return {"status_code": status.HTTP_200_OK}
