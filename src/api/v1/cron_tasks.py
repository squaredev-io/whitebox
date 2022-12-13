from src.schemas.utils import HealthCheck
from fastapi import APIRouter, status
from src.cron_tasks.monitoring_metrics import run_calculate_metrics_pipeline
from src.cron_tasks.monitoring_alerts import run_create_alerts_pipeline


cron_tasks_router = APIRouter()


@cron_tasks_router.post(
    "/cron-tasks/run",
    tags=["Cron Tasks"],
    summary="Helper endpoint",
    status_code=status.HTTP_200_OK,
    response_description="Result of cron tasks",
)
async def run_cron():
    """A helper endpoint that triggers the metrics and alerts pipelines while testing."""

    await run_calculate_metrics_pipeline()
    await run_create_alerts_pipeline()
    return HealthCheck(status="OK")
