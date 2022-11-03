import pytest
from src.tests.v1.conftest import test_order_map
from fastapi import status


@pytest.mark.order(test_order_map["health"])
def test_health(client):
    response = client.get("/v1/health")
    assert response.status_code == status.HTTP_200_OK
