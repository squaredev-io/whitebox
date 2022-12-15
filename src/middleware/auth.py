from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from src import crud
from src.schemas.user import User
from src.core.db import get_db
from src.utils.passwords import passwords_match


async def authenticate_user(
    api_key: str = Header(),
    db: Session = Depends(get_db),
) -> User:

    user = crud.users.get_first_by_filter(db, username="admin")
    if not passwords_match(user.api_key, api_key):
        raise HTTPException(
            detail="Invalid API key", status_code=status.HTTP_401_UNAUTHORIZED
        )
    return user
