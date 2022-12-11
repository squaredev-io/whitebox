import os
from whitebox.core.manager import get_task_manager
from whitebox.cron_tasks.monitoring_metrics import run_calculate_metrics_pipeline

task_manager = get_task_manager()

metrics_cron = os.getenv("METRICS_CRON") or "*/15 * * * *"

task_manager.register(
    name="metrics_cron",
    async_callable=run_calculate_metrics_pipeline,
    crontab=metrics_cron,
)
