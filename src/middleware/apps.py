from fastapi import Header, Depends, HTTPException, status
from typing import Union
from src.core.db import get_db
from src.crud.apps import apps
from sqlalchemy.orm import Session

# from src.utils.errors import errors


async def get_current_app(
    app_id: Union[str, None] = Header(default=None),
    app_secret: Union[str, None] = Header(default=None),
    db: Session = Depends(get_db),
):
    app = apps.get(db, app_id)
    if not app:
        raise HTTPException(
            detail="No valid app id", status_code=status.HTTP_404_NOT_FOUND
        )

    if app.secret == app_secret:
        return app
    else:
        raise HTTPException(
            detail="Not valid app secret", status_code=status.HTTP_400_BAD_REQUEST
        )
