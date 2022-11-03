from typing import List
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from src.schemas.utils import ErrorProps
from src.utils.logger import log


class CustomError(BaseException):
    async def http_exception_handler(self, _: Request, exc: StarletteHTTPException) -> ErrorProps:
        log.error(f"{exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(
                {"error": f"{str(exc.detail)}", "status_code": exc.status_code}
            ),
        )

    async def validation_exception_handler(
        self,
        _: Request,
        exc: HTTPException,
    ) -> ErrorProps:
        if len(exc.errors()[0]["loc"]) > 1:
            responsible_value = exc.errors()[0]["loc"][1]
        else:
            responsible_value = exc.errors()[0]["loc"][0]
        reason = exc.errors()[0]["msg"]
        log.error(f"{status.HTTP_400_BAD_REQUEST}: ({str(responsible_value)}) {str(reason)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {
                    "error": f"({str(responsible_value)}) {str(reason)}",
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                }
            ),
        )

    def bad_request(self, msg: str = "Bad request") -> ErrorProps:
        log.error(f"{status.HTTP_400_BAD_REQUEST}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_400_BAD_REQUEST}
            ),
        )

    def unauthorized(self, msg: str = "Unauthorized action") -> ErrorProps:
        log.error(f"{status.HTTP_401_UNAUTHORIZED}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_401_UNAUTHORIZED}
            ),
        )

    def not_found(self, msg: str = "Content not found") -> ErrorProps:
        log.error(f"{status.HTTP_404_NOT_FOUND}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_404_NOT_FOUND}
            ),
        )

    def content_exists(self, msg: str = "This content exists already") -> ErrorProps:
        log.error(f"{status.HTTP_409_CONFLICT}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_409_CONFLICT}
            ),
        )

    def content_gone(self, msg: str = "Content gone") -> ErrorProps:
        log.error(f"{status.HTTP_410_GONE}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_410_GONE}
            ),
        )

    def unknown_error(self, msg: str = "An unknown error was encountered") -> ErrorProps:
        log.error(f"{status.HTTP_500_INTERNAL_SERVER_ERROR}: {str(msg)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {
                    "error": str(msg),
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            ),
        )


errors = CustomError()


def formatError(e):
    e = str(e.args[0])
    if "DETAIL:" in e:
        e = e.split(":")[1].strip()
    else:
        e = e.split("\n")[0].split(")")[1].strip().capitalize()
    return e


def add_error_responses(status_codes) -> List[ErrorProps]:
    """
    For the schema to work the part after schemas/ should correspond to a title error schema in src/api/app/v1/docs.py
    """

    error_responses = {
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/BadRequest"}}
            },
        },
        401: {
            "description": "Authorization Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/AuthorizationError"}}
            },
        },
        404: {
            "description": "Not Found Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/NotFoundError"}}
            },
        },
        409: {
            "description": "Conflict Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/ConflictError"}}
            },
        },
        410: {
            "description": "Content Gone",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/ContenGone"}}
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}
            },
        },
    }
    responses = {}
    for code in status_codes:
        responses[code] = error_responses[code]
    return responses