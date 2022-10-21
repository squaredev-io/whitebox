from src.schemas.user import UserInDb, UserCreate, UserUpdate
from fastapi import APIRouter, Depends, status
from src.crud.users import user
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.utils.passwords import hash_password
from src.middleware.auth import get_current_user
from src.utils.errors import errors

users_router = APIRouter()


# TODO Reject requests from already logged in users
@users_router.post("/users", response_model=UserInDb, summary="Create user")
async def create_user(form: UserCreate, db: Session = Depends(get_db)) -> UserInDb:
    if form is not None:
        is_registered = user.get_by_email(db=db, email=form.email) is not None
        if is_registered:
            return errors.content_exists("Already registered")
        else:
            form.password = hash_password(form.password)
            new_user = user.create(db=db, obj_in=form)
            return new_user.__dict__
    else:
        return errors.bad_request("Form should not be empty")


@users_router.get("/users/{user_id}", response_model=UserInDb, summary="Get user by id")
async def get_user(
    user_id: str, db: Session = Depends(get_db)
):
    user_in_db = user.get(db=db, _id=user_id)
    if not user_in_db:
        return errors.not_found("User not found")

    return user_in_db.__dict__


@users_router.put("/users/{user_id}", response_model=UserInDb, summary="Update user")
async def update_user(
    form: UserUpdate,
    db: Session = Depends(get_db),
    curr_user: UserInDb = Depends(get_current_user),
) -> UserInDb:
    if not curr_user:
        return errors.unauthorized()
    if form is not None:
        return user.update(
            db=db, db_obj=user.get(db, curr_user["id"]), form=form
        ).__dict__
    else:
        return errors.bad_request("Form should not be empty")


@users_router.delete("/users/{user_id}", response_model=str, summary="Delete user")
async def delete_user(
    db: Session = Depends(get_db), curr_user: UserInDb = Depends(get_current_user)
) -> str:
    user.delete_account(db=db, _id=curr_user["id"])
    return status.HTTP_200_OK
