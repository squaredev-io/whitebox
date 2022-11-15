import pytest
from src.tests.v1.conftest import test_order_map
from fastapi import status


@pytest.mark.order(test_order_map["cron_tasks"]["run"])
def test_cron_tasks(client):
    response = client.post("/v1/cron_tasks/run")
    assert response.status_code == status.HTTP_200_OK
