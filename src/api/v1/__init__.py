from fastapi import APIRouter
from .health import health_router
from .auth import auth_router
from .users import users_router
from .projects import projects_router

v1_router = APIRouter()
v1 = "/v1"

v1_router.include_router(health_router, prefix=v1)
v1_router.include_router(auth_router, prefix=v1)
v1_router.include_router(users_router, prefix=v1)
v1_router.include_router(projects_router, prefix=v1)
