from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.datasetRow import DatasetRow, DatasetRowCreate
from src.entities.DatasetRow import DatasetRow as DatasetRowEntity


class CRUD(CRUDBase[DatasetRow, DatasetRowCreate, Any]):
    def get_dataset_rows(self, db: Session, *, model_id: str) -> List[DatasetRow]:
        return db.query(self.model).filter(DatasetRowEntity.model_id == model_id).all()


dataset_rows = CRUD(DatasetRowEntity)
