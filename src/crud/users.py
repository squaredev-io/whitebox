from src.utils.passwords import passwords_match
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.user import User, UserCreateDto, UserUpdateDto
from src.entities.User import User as UserEntity


class CRUD(CRUDBase[User, UserCreateDto, UserUpdateDto]):
    def authenticate(self, db: Session, *, api_key: str) -> Optional[User]:
        if not api_key:
            return None
        admin = self.get_first_by_filter(db, username="admin")
        if not passwords_match(admin.api_key, api_key):
            return None
        return admin


users = CRUD(UserEntity)
