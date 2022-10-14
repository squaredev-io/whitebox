from fastapi import FastAPI
from src.api.simulator.v1 import endpoints

from src.core.settings import get_simulator_settings
from fastapi.openapi.utils import get_openapi
import json
from src.api.simulator.v1.docs import description, tags_metadata

settings = get_simulator_settings()

simulator_app = FastAPI(title=settings.APP_NAME_SIMULATOR, redoc_url="/")


simulator_app.include_router(endpoints.v1)


def app_openapi():
    if simulator_app.openapi_schema:
        return simulator_app.openapi_schema
    openapi_schema = get_openapi(
        title="App Simulator API",
        version=settings.VERSION,
        routes=simulator_app.routes,
        description=description,
        tags=tags_metadata,
    )
    with open("src/assets/openapi_simulator.json", "r") as openapi:
        openapi = json.load(openapi)
        logo = openapi["info"]["x-logo"]
    openapi_schema["info"]["x-logo"] = logo

    simulator_app.openapi_schema = openapi_schema
    return simulator_app.openapi_schema


simulator_app.openapi = app_openapi
