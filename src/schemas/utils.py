from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str


class StatusCode(BaseModel):
    status_code: str
