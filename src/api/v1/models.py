from typing import List
from src.schemas.model import Model, ModelCreate, ModelUpdate
from fastapi import APIRouter, Depends, status
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.utils import StatusCode
from src.utils.errors import errors


models_router = APIRouter()


@models_router.post(
    "/models",
    tags=["Models"],
    response_model=Model,
    summary="Create model")
async def create_model(form: ModelCreate, db: Session = Depends(get_db)) -> Model:
    if form is not None:
        new_model = models.create(db=db, obj_in=form)
        return new_model.__dict__
    else:
        return errors.bad_request("Form should not be empty")


@models_router.get(
    "/models",
    tags=["Models"],
    response_model=List[Model],
    summary="Get all models"
)
async def get_all_models(
    db: Session = Depends(get_db)
):
    models_in_db = [_.__dict__ for _ in models.get_all(db=db)]
    if not models_in_db:
        return errors.not_found("No model found in database")

    return models_in_db


@models_router.get(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model,
    summary="Get model by id"
)
async def get_model(
    model_id: str, db: Session = Depends(get_db)
):
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")

    return model.__dict__


@models_router.put(
    "/models/{model_id}",
    tags=["Models"],
    response_model=Model, 
    summary="Update model"
)
async def update_model(
    model_id: str,
    form: ModelUpdate,
    db: Session = Depends(get_db),
) -> Model:
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")
        
    if form is not None:
        return models.update(
            db=db, db_obj=model, obj_in=form).__dict__
    else:
        return errors.bad_request("Form should not be empty")


@models_router.delete(
    "/models/{model_id}",
    tags=["Models"],
    response_model=StatusCode,
    summary="Delete user"
)
async def delete_user(
    model_id: str,
    db: Session = Depends(get_db),
) -> StatusCode:
    model = models.get(db=db, _id=model_id)
    if not model:
        return errors.not_found("Model not found")
    
    models.remove(db=db, _id=model_id)
    return {"status_code": status.HTTP_200_OK }
