from fastapi import FastAPI, Depends
import asyncio
import json
from src.utils.logger import cronLogger as logger

from src.core.settings import get_cron_settings
from src.cron_tasks.tasks import task_manager
from fastapi.openapi.utils import get_openapi


settings = get_cron_settings()
cron_app = FastAPI(title=settings.APP_NAME_CRON, redoc_url="/")


@cron_app.on_event("startup")
async def init():
    # Start task amanager
    asyncio.get_event_loop().create_task(task_manager.run())


@cron_app.on_event("shutdown")
async def shutdown():
    logger.info("App is shutting down...")
    logger.info("Task Manager is shutting down...")
    await task_manager.shutdown()


def app_openapi():
    if cron_app.openapi_schema:
        return cron_app.openapi_schema
    openapi_schema = get_openapi(
        title="Cron API", version=settings.VERSION, routes=cron_app.routes
    )

    cron_app.openapi_schema = openapi_schema
    return cron_app.openapi_schema


cron_app.openapi = app_openapi
