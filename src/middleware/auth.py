from typing import Union
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from src import crud
from src.core.db import get_db
from src.utils.passwords import passwords_match


async def authenticate_user(
    api_key: Union[str, None] = Header(default=None),
    db: Session = Depends(get_db),
) -> bool:
    if not api_key:
        raise HTTPException(
            detail="No API key provided", status_code=status.HTTP_401_UNAUTHORIZED
        )

    admin = crud.users.get_first_by_filter(db, username="admin")
    if not passwords_match(admin.api_key, api_key):
        raise HTTPException(
            detail="Invalid API key", status_code=status.HTTP_401_UNAUTHORIZED
        )
    return True
