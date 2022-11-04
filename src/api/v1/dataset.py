from typing import List
from src.schemas.dataset import Dataset, DatasetCreate
from fastapi import APIRouter, Depends, status, HTTPException
from src.crud.datasets import datasets
from src.crud.users import users
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.utils import StatusCode
from src.utils.errors import add_error_responses, errors


datasets_router = APIRouter()


@datasets_router.post(
    "/datasets/metadata",
    tags=["Datasets"],
    response_model=Dataset,
    summary="Create dataset",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 404, 409]),
)
async def create_dataset(body: DatasetCreate, db: Session = Depends(get_db)) -> Dataset:
    user = users.get(db=db, _id=body.__dict__["user_id"])
    if user:
        new_dataset = datasets.create(db=db, obj_in=body)
        return new_dataset
    else:
        return errors.not_found(f"User with id: {body.__dict__['user_id']} not found")


@datasets_router.get(
    "/datasets/{dataset_id}",
    tags=["Datasets"],
    response_model=Dataset,
    summary="Get dataset by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = datasets.get(db=db, _id=dataset_id)
    if not dataset:
        return errors.not_found("Dataset not found")

    return dataset
