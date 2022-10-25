from fastapi.encoders import jsonable_encoder
from typing import Any, Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.inference import InferenceCreate
from src.entities.Inference import Inference


class CRUD(CRUDBase[Inference, InferenceCreate, Any]):
    pass


inferences = CRUD(Inference)
