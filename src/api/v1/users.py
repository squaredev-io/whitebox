from typing import List
from src.schemas.user import User, UserCreateDto, UserUpdateDto
from fastapi import APIRouter, Depends, status
from src import crud
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.utils import StatusCode
from src.utils.passwords import hash_password
from src.utils.errors import add_error_responses, errors

users_router = APIRouter()


# TODO Reject requests from already logged in users
@users_router.post(
    "/users",
    tags=["Users"],
    response_model=User,
    summary="Create user",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 409]),
)
async def create_user(body: UserCreateDto, db: Session = Depends(get_db)) -> User:
    if body is not None:
        body.api_key = hash_password(body.api_key)
        new_user = crud.users.create(db=db, obj_in=body)
        return new_user
    else:
        return errors.bad_request("Form should not be empty")


@users_router.get(
    "/users",
    tags=["Users"],
    response_model=List[User],
    summary="Get all users",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_all_users(db: Session = Depends(get_db)):
    users_in_db = crud.users.get_all(db=db)
    if not users_in_db:
        return errors.not_found("No user found in database")

    return users_in_db


@users_router.get(
    "/users/{user_id}",
    tags=["Users"],
    response_model=User,
    summary="Get user by id",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.users.get(db=db, _id=user_id)
    if not user:
        return errors.not_found("User not found")

    return user


@users_router.put(
    "/users/{user_id}",
    tags=["Users"],
    response_model=User,
    summary="Update user",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([400, 404]),
)
async def update_user(
    user_id: str,
    body: UserUpdateDto,
    db: Session = Depends(get_db),
) -> User:
    if body is not None:
        return crud.users.update(db=db, db_obj=crud.users.get(db, user_id), obj_in=body)
    else:
        return errors.bad_request("Form should not be empty")


@users_router.delete(
    "/users/{user_id}",
    tags=["Users"],
    response_model=StatusCode,
    summary="Delete user",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> StatusCode:
    crud.users.remove(db=db, _id=user_id)
    return {"status_code": status.HTTP_200_OK}
