from typing import List, Union
from src.schemas.datasetRow import DatasetRow, DatasetRowCreate
from fastapi import APIRouter, Depends, status, Header
from src.crud.dataset_rows import dataset_rows
from src.crud.models import models
from src.crud.users import users
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.errors import add_error_responses, errors


dataset_rows_router = APIRouter()


@dataset_rows_router.post(
    "/dataset_rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Create dataset rows",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 404, 409]),
)
async def create_dataset_rows(
    body: List[DatasetRowCreate],
    db: Session = Depends(get_db),
    api_key: Union[str, None] = Header(default=None),
) -> DatasetRow:
    authenticated = users.match_api_key(db, api_key=api_key)
    if not authenticated:
        return errors.unauthorized()

    model = models.get(db=db, _id=dict(body[0])["model_id"])
    if model:
        new_dataset_rows = dataset_rows.create_many(db=db, obj_list=body)
        return new_dataset_rows
    else:
        return errors.not_found(f"Model with id: {dict(body[0])['model_id']} not found")


@dataset_rows_router.get(
    "/{model_id}/dataset_rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Get all model's dataset rows",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_dataset_rows(
    model_id: str,
    db: Session = Depends(get_db),
    api_key: Union[str, None] = Header(default=None),
):
    authenticated = users.match_api_key(db, api_key=api_key)
    if not authenticated:
        return errors.unauthorized()

    model = models.get(db, model_id)
    if model:
        return dataset_rows.get_dataset_rows(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")
