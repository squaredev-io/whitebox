from src.utils.passwords import hash_password, passwords_match
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas import Client, ClientCreate, ClientUpdate
from fastapi.encoders import jsonable_encoder
from src.crud.apps import apps
from src.models.Model import Client as ClientModel


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Client]:
        return db.query(ClientModel).filter(ClientModel.email == email).first()

    def create(self, db: Session, *, obj_in: ClientCreate) -> Client:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, form: ClientUpdate, db_obj: ClientModel) -> Client:
        if form.password:
            form.password = hash_password(form.password)

        return super().update(db=db, db_obj=db_obj, obj_in=form)

    def delete_account(self, db: Session, *, _id: str):
        apps.delete_all_apps(db, _id)
        super().remove(db, _id=_id)
        return

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[Client]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not passwords_match(user.password, password):
            return None
        return user


client = CRUDClient(ClientModel)
