import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number
from fastapi import status


@pytest.mark.order(get_order_number("health"))
def test_health(client):
    response = client.get("/v1/health")
    assert response.status_code == status.HTTP_200_OK
    validated = schemas.HealthCheck(**response.json())
