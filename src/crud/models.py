from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.model import Model, ModelCreate, ModelUpdate
from src.models.Model import Model as ModelModel


class CRUD(CRUDBase[ModelModel, ModelCreate, ModelUpdate]):
    pass


models = CRUD(ModelModel)
