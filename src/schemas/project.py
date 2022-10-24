from typing import Optional
from pydantic import BaseModel
from src.schemas.base import ItemBase


class ProjectBase(BaseModel):
    user_id: str
    name: str


class Project(ProjectBase, ItemBase):
    pass


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str
