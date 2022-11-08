from fastapi.encoders import jsonable_encoder
from typing import Optional, Any
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.dataset import Dataset, DatasetCreateDto
from src.entities.Dataset import Dataset as DatasetEntity


class CRUD(CRUDBase[Dataset, DatasetCreateDto, Any]):
    pass


datasets = CRUD(DatasetEntity)
