from typing import Any, List
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from whitebox.crud.base import CRUDBase
from whitebox.schemas.inferenceRow import InferenceRow, InferenceRowPreDb
from whitebox.entities.Inference import InferenceRow as InferenceRowEntity


class CRUD(CRUDBase[InferenceRow, InferenceRowPreDb, Any]):
    def get_inference_rows_by_model(
        self, db: Session, *, model_id: str
    ) -> List[InferenceRow]:
        return (
            db.query(self.model).filter(InferenceRowEntity.model_id == model_id).all()
        )

    def get_unused_inference_rows(
        self, db: Session, *, model_id: str
    ) -> List[InferenceRow]:
        return (
            db.query(self.model)
            .filter(
                InferenceRowEntity.model_id == model_id,
                InferenceRowEntity.is_used == False,
            )
            .all()
        )

    def get_inference_rows_betweet_dates(
        self, db: Session, *, model_id: str, min_date: datetime, max_date: datetime
    ) -> List[InferenceRow]:
        return (
            db.query(self.model)
            .filter(
                and_(
                    InferenceRowEntity.model_id == model_id,
                    InferenceRowEntity.is_used == True,
                    InferenceRowEntity.timestamp >= min_date,
                    InferenceRowEntity.timestamp < max_date,
                )
            )
            .all()
        )


inference_rows = CRUD(InferenceRowEntity)
