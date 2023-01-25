from whitebox.schemas.utils import HealthCheck
from fastapi import APIRouter, status

health_router = APIRouter()


@health_router.get(
    "/health",
    tags=["Health"],
    response_model=HealthCheck,
    summary="Health check the service",
    status_code=status.HTTP_200_OK,
    response_description="Status of the service",
)
def health_check():
    """Responds with the status of the service."""
    return HealthCheck(status="OK")
