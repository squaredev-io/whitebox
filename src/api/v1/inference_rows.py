from typing import Dict, List
from src.middleware.auth import authenticate_user
from src.schemas.inferenceRow import InferenceRow, InferenceRowCreateDto
from src.analytics.xai_models.pipelines import (
    create_xai_pipeline_classification_per_inference_row,
)
import pandas as pd
from src.schemas.user import User
from fastapi import APIRouter, Depends, status
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.errors import add_error_responses, errors


inference_rows_router = APIRouter()


@inference_rows_router.post(
    "/inference-rows",
    tags=["Inference Rows"],
    response_model=InferenceRow,
    summary="Create an inference row",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 409]),
)
async def create_row(
    body: InferenceRowCreateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> InferenceRow:

    if body is not None:
        new_inference_row = crud.inference_rows.create(db=db, obj_in=body)
        return new_inference_row
    else:
        return errors.bad_request("Body should not be empty")


@inference_rows_router.post(
    "/inference-rows/many",
    tags=["Inference Rows"],
    response_model=List[InferenceRow],
    summary="Create many inference rows",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 409]),
)
async def create_many_inference_rows(
    body: List[InferenceRowCreateDto],
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> List[InferenceRow]:

    if body is not None:
        new_inference_rows = crud.inference_rows.create_many(db=db, obj_list=body)
        return new_inference_rows
    else:
        return errors.bad_request("Form should not be empty")


@inference_rows_router.get(
    "/models/{model_id}/inference-rows",
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

    model = crud.models.get(db, model_id)
    if model:
        return crud.inference_rows.get_model_inference_rows(db=db, model_id=model_id)
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
async def create_dataset_rows(
    inference_row_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    try:
        inference_row = crud.inference_rows.get(db=db, _id=inference_row_id)
        model = crud.models.get(db=db, _id=inference_row.model_id)
        dataset_rows = crud.dataset_rows.get_dataset_rows(db=db, model_id=model.id)

        xai_report = create_xai_pipeline_classification_per_inference_row(
            training_set=pd.DataFrame(dataset_rows),
            target=model.prediction,
            inference_row=pd.DataFrame(inference_row),
            type_of_task=model.type,
        )
        return xai_report
    except:
        return errors.not_found(
            f"Couldn't create the explainability report because some data are missing!"
        )
