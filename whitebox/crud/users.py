from typing import Any
from whitebox.crud.base import CRUDBase
from whitebox.schemas.user import User, UserCreateDto
from whitebox.entities.User import User as UserEntity


class CRUD(CRUDBase[User, UserCreateDto, Any]):
    pass


users = CRUD(UserEntity)
