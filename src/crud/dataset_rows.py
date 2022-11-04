from fastapi.encoders import jsonable_encoder
from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.datasetRow import DatasetRow, DatasetRowCreate
from src.entities.DatasetRow import DatasetRow as DatasetRowEntity
import datetime


class CRUD(CRUDBase[DatasetRow, DatasetRowCreate, Any]):
    def create_many(self, db: Session, *, obj_list: List[DatasetRowCreate]) -> List[DatasetRow]:
        date_now = datetime.datetime.utcnow()
        obj_list_in_data = jsonable_encoder(obj_list)
        db_obj_list = list(map(lambda x: self.model(**x, created_at=date_now, updated_at=date_now), obj_list_in_data))
        db.add_all(db_obj_list)
        db.commit()
        return db_obj_list

    def get_dataset_rows(
        self, db: Session, *, dataset_id: int
    ) -> List[DatasetRow]:
        return (
            db.query(self.model)
            .filter(DatasetRowEntity.dataset_id == dataset_id)
            .all()
        )

dataset_rows = CRUD(DatasetRowEntity)
