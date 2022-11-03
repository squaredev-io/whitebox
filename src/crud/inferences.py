from fastapi.encoders import jsonable_encoder
from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.inference import Inference, InferenceCreate
from src.entities.Inference import Inference as InferenceEntity
import datetime


class CRUD(CRUDBase[Inference, InferenceCreate, Any]):
    def create_many(self, db: Session, *, obj_list: List[InferenceCreate]) -> List[Inference]:
        date_now = datetime.datetime.utcnow()
        obj_list_in_data = jsonable_encoder(obj_list)
        db_obj_list = list(map(lambda x: self.model(**x, created_at=date_now, updated_at=date_now), obj_list_in_data))
        db.add_all(db_obj_list)
        db.commit()
        return db_obj_list

    def get_model_inferences(
        self, db: Session, *, model_id: int
    ) -> List[Inference]:
        return (
            db.query(self.model)
            .filter(InferenceEntity.model_id == model_id)
            .all()
        )

inferences = CRUD(InferenceEntity)
