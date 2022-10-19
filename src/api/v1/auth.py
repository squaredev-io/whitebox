from requests import Session
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.core.db import get_db
from src.utils.tokens import create_access_token
from src.middleware.auth import get_current_user
from src.crud.users import user
from src.schemas.auth import Token
from src.schemas.user import UserInDb
from src.utils.errors import errors

auth_router = APIRouter()


@auth_router.post(
    "/auth/token",
    tags=["Auth"],
    summary="Get access token",
    response_model=Token,
)
async def get_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    fetched_user = user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not fetched_user:
        return errors.not_found("No user found")

    return {
        "access_token": create_access_token(fetched_user),
        "token_type": "bearer",
    }


@auth_router.post(
    "/auth/me",
    tags=["Auth"],
    summary="Get active user",
    response_model=UserInDb
)
async def get_active_user(active_user: UserInDb = Depends(get_current_user)):
    if not active_user:
        return errors.unauthorized("Not logged in")
    active_user["password"] = None
    return active_user
