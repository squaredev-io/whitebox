from typing import Dict, List
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.inferenceRow import InferenceRow, InferenceRowCreateDto
from whitebox.analytics.xai_models.pipelines import (
    create_xai_pipeline_classification_per_inference_row,
)
import pandas as pd
from whitebox.schemas.user import User
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.utils.errors import add_error_responses, errors


inference_rows_router = APIRouter()


@inference_rows_router.post(
    "/inference-rows",
    tags=["Inference Rows"],
    response_model=InferenceRow,
    summary="Create an inference row",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401]),
)
async def create_row(
    body: InferenceRowCreateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> InferenceRow:
    """Inserts an inference row into the database."""

    new_inference_row = crud.inference_rows.create(db=db, obj_in=body)
    return new_inference_row


@inference_rows_router.post(
    "/inference-rows/batch",
    tags=["Inference Rows"],
    response_model=List[InferenceRow],
    summary="Create many inference rows",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401]),
)
async def create_many_inference_rows(
    body: List[InferenceRowCreateDto],
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> List[InferenceRow]:
    """Inserts a set of inference rows into the database."""

    new_inference_rows = crud.inference_rows.create_many(db=db, obj_list=body)
    return new_inference_rows


@inference_rows_router.get(
    "/inference-rows",
    tags=["Inference Rows"],
    response_model=List[InferenceRow],
    summary="Get all model's inference rows",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_inference_rows(
    model_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """Fetches the inference rows of a specific model. A model id is required."""

    model = crud.models.get(db, model_id)
    if model:
        return crud.inference_rows.get_inference_rows_by_model(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")


@inference_rows_router.get(
    "/inference-rows/{inference_row_id}",
    tags=["Inference Rows"],
    response_model=InferenceRow,
    summary="Get inference row by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_inference_row(
    inference_row_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """Fetches a specific inference row. An inference row id is required."""

    inference_row = crud.inference_rows.get(db=db, _id=inference_row_id)
    if not inference_row:
        return errors.not_found("Inference not found")

    return inference_row


@inference_rows_router.get(
    "/inference-rows/{inference_row_id}/xai",
    tags=["Inference Rows"],
    response_model=Dict[str, float],
    summary="Creates and fetches am explainability report for an inference row",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def create_inference_row_xai_report(
    inference_row_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """
    Given a specific inference row id, this endpoint produces an explainability report for this inference.
    The XAI pipeline requires a set of dataset rows as a training set, a model and the inference row.
    If one of those three is not found in the database, a 404 error is returned.
    """

    inference_row = crud.inference_rows.get(db=db, _id=inference_row_id)
    if not inference_row:
        return errors.not_found(f"Inference row with id {inference_row_id} not found")

    inference_row_df = pd.DataFrame([inference_row.processed])
    inference_row_series = inference_row_df.drop(columns=["target"]).iloc[0]

    model = crud.models.get(db=db, _id=inference_row.model_id)
    if not model:
        return errors.not_found(f"Model with id {inference_row.model_id} not found")

    dataset_rows = crud.dataset_rows.get_dataset_rows_by_model(db=db, model_id=model.id)
    if not dataset_rows:
        return errors.not_found(
            f"Dataset rows for model with id {inference_row.model_id} not found"
        )

    dataset_rows_processed = [x.processed for x in dataset_rows]

    xai_report = create_xai_pipeline_classification_per_inference_row(
        training_set=pd.DataFrame(dataset_rows_processed),
        target=model.prediction,
        inference_row=inference_row_series,
        type_of_task=model.type,
        model_id=model.id,
    )

    return xai_report
