from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.models.App import App as AppModel
from src.schemas import App, AppCreate, AppUpdate, Catalog
from src.utils.passwords import generate_app_secret


class CRUDApp(CRUDBase[App, AppCreate, AppUpdate]):
    def create_app(self, db: Session, client_id: int, *, obj_in: AppCreate) -> App:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            client_id=client_id,
            secret=generate_app_secret(),
            catalog_id=None
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_apps(
        self, db: Session, *, client_id: str, skip: int = 0, limit: int = 100
    ) -> List[App]:
        return (
            db.query(self.model)
            .filter(AppModel.client_id == client_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete_all_apps(self, db: Session, client_id: str):
        db.query(self.model).filter(self.model.client_id == client_id).delete()
        db.commit()
        return

    def map_app_to_catalog(self, db: Session, app: App, catalog_id: str):
        app.catalog_id = catalog_id
        db.commit()
        return

    def unmap_app_to_catalog(self, db: Session, app: App, catalog: Catalog):
        catalog.app_id = None
        app.catalog_id = None
        db.commit()
        return


apps = CRUDApp(AppModel)
