from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.requests import Request


class CustomError(BaseException):
    async def http_exception_handler(self, _: Request, exc: StarletteHTTPException):
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
    ):
        if len(exc.errors()[0]["loc"]) > 1:
            responsible_value = exc.errors()[0]["loc"][1]
        else:
            responsible_value = exc.errors()[0]["loc"][0]
        reason = exc.errors()[0]["msg"]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {
                    "error": f"({str(responsible_value)}) {str(reason)}",
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                }
            ),
        )

    def bad_request(self, msg: str = "Bad request"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_400_BAD_REQUEST}
            ),
        )

    def unauthorized(self, msg: str = "Unauthorized action"):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_401_UNAUTHORIZED}
            ),
        )

    def not_found(self, msg: str = "Content not found"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_404_NOT_FOUND}
            ),
        )

    def content_gone(self, msg: str = "Content gone"):
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_410_GONE}
            ),
        )

    def content_exists(self, msg: str = "This content exists already"):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder(
                {"error": str(msg), "status_code": status.HTTP_409_CONFLICT}
            ),
        )

    def unknown_error(self, msg: str = "An unknown error was encountered"):
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
