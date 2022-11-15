from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.inferenceRow import InferenceRow, InferenceRowCreateDto
from src.entities.Inference import InferenceRow as InferenceEntity


class CRUD(CRUDBase[InferenceRow, InferenceRowCreateDto, Any]):
    def get_model_inference_rows(
        self, db: Session, *, model_id: str
    ) -> List[InferenceRow]:
        return db.query(self.model).filter(InferenceEntity.model_id == model_id).all()


inference_rows = CRUD(InferenceEntity)
