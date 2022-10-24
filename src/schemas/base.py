import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime