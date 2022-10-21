from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import v1_router
from fastapi.openapi.utils import get_openapi
import json
from src.core.settings import get_settings
from src.core.db import connect, close
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from src.utils.errors import errors

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, redoc_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


app.add_exception_handler(StarletteHTTPException, errors.http_exception_handler)
app.add_exception_handler(RequestValidationError, errors.validation_exception_handler)


@app.on_event("startup")
async def on_app_start():
    """Anything that needs to be done while app starts"""
    await connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    """Anything that needs to be done while app shutdown"""
    await close()


def app_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Whitebox",
        version=settings.VERSION,
        routes=app.routes,
    )
    # with open("src/assets/openapi.json", "r") as openapi:
    #     openapi = json.load(openapi)
    #     logo = openapi["info"]["x-logo"]
    # openapi_schema["info"]["x-logo"] = logo

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = app_openapi
