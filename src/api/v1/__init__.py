from fastapi import APIRouter
from .health import health_router
from .auth import auth_router
from .users import users_router
from .models import models_router
from .dataset import datasets_router
from .dataset_rows import dataset_rows_router
from .inference_rows import inference_rows_router
from .performance_metrics import performance_metrics_router
from .drifting_metrics import drifting_metrics_router
from .model_integrity_metrics import model_integrity_metrics_router


v1_router = APIRouter()
v1 = "/v1"

v1_router.include_router(health_router, prefix=v1)
v1_router.include_router(auth_router, prefix=v1)
v1_router.include_router(users_router, prefix=v1)
v1_router.include_router(models_router, prefix=v1)
v1_router.include_router(datasets_router, prefix=v1)
v1_router.include_router(dataset_rows_router, prefix=v1)
v1_router.include_router(inference_rows_router, prefix=v1)
v1_router.include_router(performance_metrics_router, prefix=v1)
v1_router.include_router(drifting_metrics_router, prefix=v1)
v1_router.include_router(model_integrity_metrics_router, prefix=v1)
