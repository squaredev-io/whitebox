from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.schemas.project import Project, ProjectCreate, ProjectUpdate
from src.entities.Project import Project as ProjectModel


class CRUD(CRUDBase[ProjectModel, ProjectCreate, ProjectUpdate]):
    pass


projects = CRUD(ProjectModel)
