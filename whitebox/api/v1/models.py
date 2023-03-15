from typing import List
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.model import Model, ModelCreateDto, ModelUpdateDto
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.schemas.utils import StatusCode
from whitebox.schemas.user import User
from whitebox.utils.errors import add_error_responses, errors


models_router = APIRouter()


@models_router.post(
    "/models",
    tags=["Models"],
    response_model=Model,
    summary="Create model",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401]),
)
async def create_model(
    body: ModelCreateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> Model:
    """Inserts a model into the database"""

    new_model = crud.models.create(db=db, obj_in=body)
    return new_model


@models_router.get(
    "/models",
    tags=["Models"],
    response_model=List[Model],
    summary="Get all models",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401]),
)
async def get_all_models(
    db: Session = Depends(get_db), authenticated_user: User = Depends(authenticate_user)
):
    """Fetches all models from the database"""

    models_in_db = crud.models.get_all(db=db)
    return models_in_db


@models_router.get(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model,
    summary="Get model by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_model(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """Fetches the model with the specified id from the database"""

    model = crud.models.get(db=db, _id=model_id)

    if not model:
        return errors.not_found("Model not found")

    return model


@models_router.put(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model,
    summary="Update model",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([400, 401, 404]),
)
async def update_model(
    model_id: str,
    body: ModelUpdateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> Model:
    """Updates record of the model with the specified id"""

    # Remove all unset properties (with None values) from the update object
    filtered_body = {k: v for k, v in dict(body).items() if v is not None}

    model = crud.models.get(db=db, _id=model_id)

    if not model:
        return errors.not_found("Model not found")

    return crud.models.update(db=db, db_obj=model, obj_in=filtered_body)


@models_router.delete(
    "/models/{model_id}",
    tags=["Models"],
    response_model=StatusCode,
    summary="Delete model",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def delete_model(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> StatusCode:
    """Deletes the model with the specified id from the database"""

    model = crud.models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")

    crud.models.remove(db=db, _id=model_id)
    return {"status_code": status.HTTP_200_OK}
