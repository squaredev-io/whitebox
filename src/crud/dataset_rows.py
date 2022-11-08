from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.dataset import DatasetRow, DatasetRowCreate
from src.entities.DatasetRow import DatasetRow as DatasetRowEntity


class CRUD(CRUDBase[DatasetRow, DatasetRowCreate, Any]):
    def get_dataset_rows(
        self, db: Session, *, dataset_id: int
    ) -> List[DatasetRow]:
        return (
            db.query(self.model)
            .filter(DatasetRowEntity.dataset_id == dataset_id)
            .all()
        )

dataset_rows = CRUD(DatasetRowEntity)
