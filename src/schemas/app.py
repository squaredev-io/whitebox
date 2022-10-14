from pydantic import BaseModel
from typing import Optional


class App(BaseModel):
    id: str
    client_id: str
    name: str
    secret: str
    catalog_id: Optional[str]


class AppCreate(BaseModel):
    name: str


class AppUpdate(BaseModel):
    name: Optional[str]
    catalog_id: Optional[str]
