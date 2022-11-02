from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.model import Model, ModelCreate, ModelUpdate
from src.entities.Model import Model as ModelEntity


class CRUD(CRUDBase[Model, ModelCreate, ModelUpdate]):
    pass


models = CRUD(ModelEntity)
