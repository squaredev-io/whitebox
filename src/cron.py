from fastapi import FastAPI, Depends
import asyncio
import json
from src.utils.logger import cronLogger as logger
from src.api.cron.v1 import endpoints
from src.core.settings import get_cron_settings
from src.middleware.authorize_client import get_api_key
from src.cron_tasks.tasks import task_manager
from fastapi.openapi.utils import get_openapi
from src.api.cron.v1.docs import description, tags_metadata


settings = get_cron_settings()
cron_app = FastAPI(
    title=settings.APP_NAME_CRON, redoc_url="/", dependencies=[Depends(get_api_key)]
)
cron_app.include_router(endpoints.v1)


@cron_app.on_event("startup")
async def init():
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
        title="Cron API",
        version=settings.VERSION,
        routes=cron_app.routes,
        description=description,
        tags=tags_metadata,
    )
    with open("src/assets/openapi_cron.json", "r") as openapi:
        openapi = json.load(openapi)
        logo = openapi["info"]["x-logo"]
    openapi_schema["info"]["x-logo"] = logo

    cron_app.openapi_schema = openapi_schema
    return cron_app.openapi_schema


cron_app.openapi = app_openapi
