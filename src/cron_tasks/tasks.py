import os
from src.core.manager import get_task_manager

task_manager = get_task_manager()

print_job_param = os.getenv("CATALOG_REFRESH_CRON") or "* * * * *"

async def print_job():
    print("Hello!")
    return

task_manager.register(
    name="print_job",
    async_callable=print_job,
    crontab=print_job_param,
)
