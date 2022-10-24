from src.models.User import User
from src.schemas.project import Project, ProjectCreate, ProjectUpdate
from fastapi import APIRouter, Depends, status
from src.crud.projects import projects
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.middleware.auth import get_current_user
from src.schemas.utils import StatusCode
from src.utils.errors import errors

projects_router = APIRouter()


@projects_router.post(
    "/projects",
    tags=["Projects"],
    response_model=Project,
    summary="Create project")
async def create_project(form: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    if form is not None:
        new_project = projects.create(db=db, obj_in=form)
        return new_project.__dict__
    else:
        return errors.bad_request("Form should not be empty")


@projects_router.get(
    "/projects/{project_id}",
    tags=["Projects"],
    response_model=Project,
    summary="Get project by id"
)
async def get_project(
    project_id: str, db: Session = Depends(get_db)
):
    project = projects.get(db=db, _id=project_id)
    if not project:
        return errors.not_found("Project not found")

    return project.__dict__


@projects_router.put(
    "/projects/{project_id}",
    tags=["Projects"],
    response_model=Project, 
    summary="Update project"
)
async def update_project(
    project_id: str,
    form: ProjectUpdate,
    db: Session = Depends(get_db),
    # curr_user: User = Depends(get_current_user),
) -> Project:
    # if not curr_user:
    #     return errors.unauthorized()
    project = projects.get(db=db, _id=project_id)
    if not project:
        return errors.not_found("Project not found")
        
    if form is not None:
        return projects.update(
            db=db, db_obj=project, obj_in=form).__dict__
    else:
        return errors.bad_request("Form should not be empty")


@projects_router.delete(
    "/projects/{project_id}",
    tags=["Projects"],
    response_model=StatusCode,
    summary="Delete user"
)
async def delete_user(
    project_id: str,
    db: Session = Depends(get_db),
    # curr_user: User = Depends(get_current_user)
) -> StatusCode:
    # if not curr_user:
    #     return errors.unauthorized()
    project = projects.get(db=db, _id=project_id)
    if not project:
        return errors.not_found("Project not found")
    
    projects.remove(db=db, _id=project_id)
    return {"status_code": status.HTTP_200_OK }
