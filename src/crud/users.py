from src.utils.passwords import hash_password, passwords_match
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.user import User, UserCreateDto, UserUpdateDto
from src.entities.User import User as UserEntity


class CRUD(CRUDBase[User, UserCreateDto, UserUpdateDto]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(UserEntity).filter(UserEntity.email == email).first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not passwords_match(user.password, password):
            return None
        return user

    def match_api_key(self, db: Session, *, api_key: str) -> Optional[User]:
        if not api_key:
            return None
        admin = self.get_first_by_filter(db, username="admin")
        if not passwords_match(admin.api_key, api_key):
            return None
        return admin


users = CRUD(UserEntity)
