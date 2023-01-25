from typing import Any, List
from sqlalchemy.orm import Session
from whitebox.crud.base import CRUDBase
from whitebox.schemas.inferenceRow import InferenceRow, InferenceRowCreateDto
from whitebox.entities.Inference import InferenceRow as InferenceRowEntity


class CRUD(CRUDBase[InferenceRow, InferenceRowCreateDto, Any]):
    def get_inference_rows_by_model(
        self, db: Session, *, model_id: str
    ) -> List[InferenceRow]:
        return (
            db.query(self.model).filter(InferenceRowEntity.model_id == model_id).all()
        )


inference_rows = CRUD(InferenceRowEntity)
