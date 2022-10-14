from src.schemas.utils import HealthCheck
from fastapi import APIRouter

health_router = APIRouter()


@health_router.get(
    "/health",
    tags=["Health"],
    summary="Health check the service",
    response_description="Status of the service",
    response_model=HealthCheck,
)
def health_check():
    """Responds with the status of the service."""
    return HealthCheck(status="OK")
