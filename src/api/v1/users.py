from typing import List
from src.schemas.user import User, UserCreate, UserUpdate
from fastapi import APIRouter, Depends, status
from src.crud.users import users
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.utils import StatusCode
from src.utils.passwords import hash_password
from src.utils.errors import errors

users_router = APIRouter()


# TODO Reject requests from already logged in users
@users_router.post(
    "/users", 
    tags=["Users"],
    response_model=User, 
    summary="Create user"
)
async def create_user(form: UserCreate, db: Session = Depends(get_db)) -> User:
    if form is not None:
        is_registered = users.get_by_email(db=db, email=form.email) is not None
        if is_registered:
            return errors.content_exists("Already registered")
        else:
            form.password = hash_password(form.password)
            new_user = users.create(db=db, obj_in=form)
            return new_user.__dict__
    else:
        return errors.bad_request("Form should not be empty")


@users_router.get(
    "/users",
    tags=["Users"],
    response_model=List[User],
    summary="Get all users"
)
async def get_all_users(
    db: Session = Depends(get_db)
):
    users_in_db = [_.__dict__ for _ in users.get_all(db=db)]
    if not users_in_db:
        return errors.not_found("No user found in database")

    return users_in_db


@users_router.get(
    "/users/{user_id}", 
    tags=["Users"], 
    response_model=User, 
    summary="Get user by id"
)
async def get_user(
    user_id: str, db: Session = Depends(get_db)
):
    user = users.get(db=db, _id=user_id)
    if not user:
        return errors.not_found("User not found")

    return user.__dict__


@users_router.put(
    "/users/{user_id}", 
    tags=["Users"],
    response_model=User, 
    summary="Update user"
)
async def update_user(
    user_id: str,
    form: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    if form is not None:
        return users.update(
            db=db, db_obj=users.get(db, user_id), form=form
        ).__dict__
    else:
        return errors.bad_request("Form should not be empty")


@users_router.delete(
    "/users/{user_id}",
    tags=["Users"], 
    response_model=StatusCode, 
    summary="Delete user"
)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> StatusCode:
    users.remove(db=db, _id=user_id)
    return {"status_code": status.HTTP_200_OK}
