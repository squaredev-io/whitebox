from typing import List
from src.schemas.inference import Inference, InferenceCreate
from fastapi import APIRouter, Depends, status
from src.crud.inferences import inferences
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.errors import errors


inferences_router = APIRouter()


@inferences_router.post(
    "/inferences",
    tags=["Inferences"],
    response_model=Inference,
    status_code=status.HTTP_201_CREATED,
    summary="Create inference",
)
async def create_inference(
    form: InferenceCreate, db: Session = Depends(get_db)
) -> Inference:
    if form is not None:
        new_inference = inferences.create(db=db, obj_in=form)
        return new_inference
    else:
        return errors.bad_request("Form should not be empty")



@inferences_router.post(
    "/inferences/many",
    tags=["Inferences"],
    response_model=List[Inference],
    status_code=status.HTTP_201_CREATED,
    summary="Create many inference",
)
async def create_inference(
    form: List[InferenceCreate], db: Session = Depends(get_db)
) -> Inference:
    if form is not None:
        new_inference = inferences.create_many(db=db, obj_list=form)
        return new_inference
    else:
        return errors.bad_request("Form should not be empty")


@inferences_router.get(
    "/inferences",
    tags=["Inferences"],
    response_model=List[Inference],
    summary="Get all inferences",
    status_code=status.HTTP_200_OK,
)
async def get_all_inferences(db: Session = Depends(get_db)):
    inferences_in_db = inferences.get_all(db=db)
    if not inferences_in_db:
        return errors.not_found("No inference found in database")

    return inferences_in_db


@inferences_router.get(
    "/inferences/{inference_id}",
    tags=["Inferences"],
    response_model=Inference,
    status_code=status.HTTP_200_OK,
    summary="Get inference by id",
)
async def get_inference(inference_id: str, db: Session = Depends(get_db)):
    inference = inferences.get(db=db, _id=inference_id)
    if not inference:
        return errors.not_found("Inference not found")

    return inference
