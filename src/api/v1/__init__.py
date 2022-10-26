from fastapi import APIRouter
from .health import health_router
from .auth import auth_router
from .users import users_router
from .models import models_router
from .inferences import inferences_router

v1_router = APIRouter()
v1 = "/v1"

v1_router.include_router(health_router, prefix=v1)
v1_router.include_router(auth_router, prefix=v1)
v1_router.include_router(users_router, prefix=v1)
v1_router.include_router(models_router, prefix=v1)
v1_router.include_router(inferences_router, prefix=v1)
