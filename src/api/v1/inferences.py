from typing import List
from src.schemas.inference import Inference, InferenceCreate
from fastapi import APIRouter, Depends, status
from src.crud.inferences import inferences
from src.crud.models import models
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.errors import add_error_responses, errors


inferences_router = APIRouter()


@inferences_router.post(
    "/inferences",
    tags=["Inferences"],
    response_model=Inference,
    summary="Create inference",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 409]),
)
async def create_inference(
    body: InferenceCreate, db: Session = Depends(get_db)
) -> Inference:
    if body is not None:
        new_inference = inferences.create(db=db, obj_in=body)
        return new_inference
    else:
        return errors.bad_request("Body should not be empty")


@inferences_router.post(
    "/inferences/many",
    tags=["Inferences"],
    response_model=List[Inference],
    summary="Create many inference",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 409]),
)
async def create_many_inferences(
    body: List[InferenceCreate], db: Session = Depends(get_db)
) -> Inference:
    if body is not None:
        new_inference = inferences.create_many(db=db, obj_list=body)
        return new_inference
    else:
        return errors.bad_request("Form should not be empty")


@inferences_router.get(
    "/models/{model_id}/inferences",
    tags=["Inferences"],
    response_model=List[Inference],
    summary="Get all model's inferences",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_all_models_inferences(model_id: str, db: Session = Depends(get_db)):
    model = models.get(db, model_id)
    if model:
        return inferences.get_model_inferences(db=db, model_id=model_id)
    else:
        return errors.not_found("Model not found")


@inferences_router.get(
    "/inferences/{inference_id}",
    tags=["Inferences"],
    response_model=Inference,
    summary="Get inference by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_inference(inference_id: str, db: Session = Depends(get_db)):
    inference = inferences.get(db=db, _id=inference_id)
    if not inference:
        return errors.not_found("Inference not found")

    return inference
