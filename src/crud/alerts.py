from typing import Any, List
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.entities.Alert import Alert as AlertEntity
from src.schemas.alert import Alert


class CRUD(CRUDBase[Alert, Any, Any]):
    def get_model_alerts_by_model(self, db: Session, *, model_id: str) -> List[Alert]:
        return db.query(self.model).filter(AlertEntity.model_id == model_id).all()


alerts = CRUD(AlertEntity)
