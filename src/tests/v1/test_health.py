import pytest
from src.tests.v1.conftest import test_order_map


@pytest.mark.order(test_order_map["health"])
def test_health(client):
    response = client.get("/v1/health")
    assert response.json() == {"status": "OK"}
