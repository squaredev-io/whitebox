from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str


class StatusCode(BaseModel):
    status_code: str


class ErrorProps(BaseModel):
    error: str
    status_code: int


class ErrorResponse(BaseModel):
    title: str
    type: str
    properties: ErrorProps
