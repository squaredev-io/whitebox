from typing import Any
from src.crud.base import CRUDBase
from src.schemas.user import User, UserCreateDto
from src.entities.User import User as UserEntity


class CRUD(CRUDBase[User, UserCreateDto, Any]):
    pass


users = CRUD(UserEntity)
