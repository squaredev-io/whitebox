from typing import Union, List, Optional
from enum import Enum
from pydantic import BaseModel
from .app import App


class ClientRoles(str, Enum):
    admin = 'admin',
    product_owner = 'product_owner'


class Client(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    email: str
    password: Union[str, None] = None


class ClientCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str


class ClientUpdate(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    password: Union[str, None] = None
