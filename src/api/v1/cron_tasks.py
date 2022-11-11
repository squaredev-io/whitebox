from src.schemas.utils import HealthCheck
from fastapi import APIRouter, status
from src.cron_tasks.drift import run_create_data_drift_pipeline


cron_tasks_router = APIRouter()


@cron_tasks_router.post(
    "/cron_tasks/run",
    tags=["Cron Tasks"],
    summary="Helper endpoint",
    status_code=status.HTTP_200_OK,
    response_description="Result of cron jobs",
)
def run_cron():
    result = run_create_data_drift_pipeline()

    return HealthCheck(status="OK")
