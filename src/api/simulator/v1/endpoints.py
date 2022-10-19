from datetime import datetime
from enum import Enum
# from src.utils.items import parse_items
from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str

@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    response_description="Status of the service",
    response_model=HealthResponse,
)
def health_check():
    """Returns the health status of the service"""
    return dict(status="OK")


@router.get(
    "/xml/{quantity}",
    tags=["XML"],
    summary="Get xml sample",
    response_model=XMLResponse,
    response_description="XML sample",
)
async def _(quantity: int):
    generated = ""
    for _ in range(quantity):
        generated += GetXML.execute()

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<root>"
        f"<created_at>{datetime.now()}</created_at>"
        "<CATALOG>"
        f"{generated}"
        "</CATALOG>"
        "</root>"
    )
    return Response(content=xml, headers={"Content-Type": "application/xml"})


# @router.post("/validate", summary="Validate your XML")
# def _(url: str):
#     parse_items(url)
#     return {"status_code": 200, "message": "Your XML is valid!"}


@router.get("/xml/standard/{size}", summary="Standard XML sample", tags=["XML"])
def _(size: XMLSize):
    with open('src/assets/small.xml', 'r') as f:
        xml = f.read()
    f.close()
    return Response(content=xml, headers={"Content-Type": "application/xml"})


v1 = APIRouter()
v1.include_router(router, prefix="/v1")
