from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.models.Model import Client
from src.models.User import User
from sqlalchemy.orm import Session

# import schemas
from src.schemas.auth import TokenPayload

# import crud
from src.crud import users
from datetime import datetime
from src.core.db import get_db
from src.utils.tokens import decode_access_token


def is_expired(decoded: TokenPayload) -> bool:
    if not decoded:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
    expiration = datetime.strptime(
        decoded["expiration"].split(".")[0], "%Y-%m-%d %H:%M:%S"
    )
    if not expiration > datetime.utcnow():
        raise True
    return False


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    payload = decode_access_token(token)
    if is_expired(payload):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    user = users.user.get(db, _id=payload["id"])
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No user found")
    return user.__dict__
