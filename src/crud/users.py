from src.crud.base import CRUDBase
from src.schemas.user import User, UserCreateDto, UserUpdateDto
from src.entities.User import User as UserEntity


class CRUD(CRUDBase[User, UserCreateDto, UserUpdateDto]):
    pass


users = CRUD(UserEntity)
