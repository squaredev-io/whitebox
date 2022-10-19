import datetime
from pydantic import BaseModel


class ItemInDbBase(BaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime