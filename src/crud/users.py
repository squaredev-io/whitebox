from src.utils.passwords import hash_password, passwords_match
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.user import User, UserCreate, UserUpdate
from src.models.User import User as UserModel


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    def update(self, db: Session, *, form: UserUpdate, db_obj: UserModel) -> User:
        if form.password:
            form.password = hash_password(form.password)

        return super().update(db=db, db_obj=db_obj, obj_in=form)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not passwords_match(user.password, password):
            return None
        return user


users = CRUDUser(UserModel)
