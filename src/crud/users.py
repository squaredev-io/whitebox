from src.utils.passwords import hash_password, passwords_match
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.user import UserCreate, UserInDb, UserUpdate
from src.models.User import User as UserModel


class CRUDUser(CRUDBase[UserInDb, UserCreate, UserUpdate]):
    # def create(self, db: Session, obj_in: UserCreate) -> UserInDb:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj.__dict__

    def update(self, db: Session, *, form: UserUpdate, db_obj: UserModel) -> UserInDb:
        if form.password:
            form.password = hash_password(form.password)

        return super().update(db=db, db_obj=db_obj, obj_in=form)

    def delete_account(self, db: Session, *, _id: str):
        super().remove(db, _id=_id)
        return

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserInDb]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[UserInDb]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not passwords_match(user.password, password):
            return None
        return user


user = CRUDUser(UserModel)
