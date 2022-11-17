from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.model import Model, ModelCreateDto, ModelUpdateDto
from src.entities.Model import Model as ModelEntity


class CRUD(CRUDBase[Model, ModelCreateDto, ModelUpdateDto]):
    pass


models = CRUD(ModelEntity)
