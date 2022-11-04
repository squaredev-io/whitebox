from typing import List
from src.schemas.datasetRow import DatasetRow, DatasetRowCreate
from fastapi import APIRouter, Depends, status
from src.crud.dataset_rows import dataset_rows
from src.crud.datasets import datasets
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.errors import add_error_responses, errors


dataset_rows_router = APIRouter()


@dataset_rows_router.post(
    "/datasets/rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Create dataset rows",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 404, 409]),
)
async def create_dataset_rows(
    body: List[DatasetRowCreate], db: Session = Depends(get_db)
) -> DatasetRow:
    dataset = datasets.get(db=db, _id=body[0].__dict__["dataset_id"])
    if dataset:
        new_dataset_rows = dataset_rows.create_many(db=db, obj_list=body)
        return new_dataset_rows
    else:
        return errors.not_found(f"Model with id: {body[0].__dict__['dataset_id']} not found")


@dataset_rows_router.get(
    "/datasets/{dataset_id}/rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Get all dataset's rows",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_all_dataset_rows(dataset_id: str, db: Session = Depends(get_db)):
    dataset = datasets.get(db, dataset_id)
    if dataset:
        return dataset_rows.get_dataset_rows(db=db, dataset_id=dataset_id)
    else:
        return errors.not_found("Model not found")
