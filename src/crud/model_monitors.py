from typing import Any, List
from src.crud.base import CRUDBase
from sqlalchemy.orm import Session
from src.schemas.modelMonitor import ModelMonitor, ModelMonitorCreateDto
from src.entities.ModelMonitor import ModelMonitor as ModelMonitorEntity


class CRUD(CRUDBase[ModelMonitor, ModelMonitorCreateDto, Any]):
    def get_model_monitors_by_model(
        self, db: Session, *, model_id: str
    ) -> List[ModelMonitor]:
        return (
            db.query(self.model).filter(ModelMonitorEntity.model_id == model_id).all()
        )


model_monitors = CRUD(ModelMonitorEntity)
