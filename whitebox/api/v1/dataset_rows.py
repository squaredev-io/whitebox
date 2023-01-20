import pandas as pd
from typing import List
from whitebox.analytics.models.pipelines import (
    create_binary_classification_training_model_pipeline,
    create_multiclass_classification_training_model_pipeline,
)
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.datasetRow import DatasetRow, DatasetRowCreate
from whitebox.schemas.user import User
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.encoders import jsonable_encoder
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.utils.errors import add_error_responses, errors


dataset_rows_router = APIRouter()


@dataset_rows_router.post(
    "/dataset-rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Create dataset rows",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 404, 409]),
)
async def create_dataset_rows(
    body: List[DatasetRowCreate],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> DatasetRow:
    """
    Inserts a set of dataset rows into the database.
    \nWhen the dataset rows are successfully saved, the pipeline for training the model is triggered.
    """

    if len(body) <= 1:
        return errors.bad_request("Training dataset should be longer that 1 row!")

    model = crud.models.get(db=db, _id=dict(body[0])["model_id"])
    if model:
        for row in body:
            if not model.prediction in row.processed:
                return errors.bad_request(
                    f'Column "{model.prediction}" was not found in some or any of the rows in provided training dataset. Please try again!'
                )

        predictions = list(set(vars(x)["processed"][model.prediction] for x in body))
        if len(predictions) <= 1:
            return errors.bad_request(
                f'Training dataset\'s "{model.prediction}" columns must have at least 2 different values!'
            )

        new_dataset_rows = crud.dataset_rows.create_many(db=db, obj_list=body)
        processed_dataset_rows = [
            x["processed"] for x in jsonable_encoder(new_dataset_rows)
        ]
        processed_dataset_rows_pd = pd.DataFrame(processed_dataset_rows)

        if model.type == "binary":
            background_tasks.add_task(
                create_binary_classification_training_model_pipeline,
                processed_dataset_rows_pd,
                model.prediction,
                model.id,
            )
        elif model.type == "multi_class":
            background_tasks.add_task(
                create_multiclass_classification_training_model_pipeline,
                processed_dataset_rows_pd,
                model.prediction,
                model.id,
            )
        return new_dataset_rows
    else:
        return errors.not_found(f"Model with id: {dict(body[0])['model_id']} not found")


@dataset_rows_router.get(
    "/dataset-rows",
    tags=["Dataset Rows"],
    response_model=List[DatasetRow],
    summary="Get all model's dataset rows",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_dataset_rows(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """Fetches the dataset rows of a specific model. A model id is required."""

    model = crud.models.get(db, model_id)
    if model:
        return crud.dataset_rows.get_dataset_rows_by_model(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")
