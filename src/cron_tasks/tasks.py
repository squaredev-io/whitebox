import os
from src.core.manager import get_task_manager
from src.cron_tasks.monitoring_metrics import run_calculate_metrics_pipeline
from src.cron_tasks.monitoring_alerts import run_create_alerts_pipeline

task_manager = get_task_manager()

metrics_cron = os.getenv("METRICS_CRON") or "*/15 * * * *"

task_manager.register(
    name="metrics_cron",
    async_callable=run_calculate_metrics_pipeline,
    crontab=metrics_cron,
)

task_manager.register(
    name="alerts_cron",
    async_callable=run_create_alerts_pipeline,
    crontab=metrics_cron,
)
