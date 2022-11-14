from src.schemas.utils import HealthCheck
from fastapi import APIRouter, status
from src.cron_tasks.monitoring_metrics import (
    run_calculate_drifting_metrics_pipeline,
    run_calculate_performance_metrics_pipeline,
)


cron_tasks_router = APIRouter()


@cron_tasks_router.post(
    "/cron_tasks/run",
    tags=["Cron Tasks"],
    summary="Helper endpoint",
    status_code=status.HTTP_200_OK,
    response_description="Result of cron jobs",
)
async def run_cron():
    run_calculate_drifting_metrics_pipeline_result = (
        await run_calculate_drifting_metrics_pipeline()
    )
    run_calculate_performance_metrics_pipeline_result = (
        await run_calculate_performance_metrics_pipeline()
    )

    return HealthCheck(status="OK")
