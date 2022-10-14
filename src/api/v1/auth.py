from requests import Session
from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.db import get_db
from src.utils.tokens import create_access_token
from src.middleware.auth import get_current_client
from src.crud.clients import client
from src.schemas.auth import Token
from src.utils.errors import errors

auth_router = APIRouter()


@auth_router.post(
    "/auth/token",
    tags=["auth"],
    summary="Get access token",
    response_model=Token,
)
async def get_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = client.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        return errors.not_found("No client found")

    return {
        "access_token": create_access_token(user),
        "token_type": "bearer",
    }


@auth_router.post(
    "/auth/me", tags=["Auth"], summary="Get current client", response_model=Client
)
async def get_current_client(active_client: Client = Depends(get_current_client)):
    if not active_client:
        return errors.unauthorized("Not logged in")
    active_client["password"] = None
    return active_client
