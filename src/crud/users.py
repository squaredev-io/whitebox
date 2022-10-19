from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas import User, UserCreate, UserUpdate
from src.models.User import User as UserModel


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, app_id: str, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, app_id=app_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.__dict__

    def delete_all_users(self, db: Session, app_id: str):
        to_be_deleted = UserModel.__table__.delete().where(
            UserModel.User.app_id == app_id
        )
        db.execute(to_be_deleted)
        db.commit()
        return

    def get_by_ext_id(self, db: Session, ext_id: str):
        return db.query(self.model).filter(self.model.ext_id == ext_id).first()

    def remove_by_ext_id(self, db: Session, ext_id: str):
        db.query(self.model).filter(self.model.ext_id == ext_id).delete()
        db.commit()
        return


users = CRUDUser(UserModel)
