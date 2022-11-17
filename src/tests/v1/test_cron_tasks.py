import pytest
from src.tests.v1.conftest import get_order_number
from fastapi import status


@pytest.mark.order(get_order_number("cron_tasks_run"))
def test_cron_tasks(client):
    response = client.post("/v1/cron_tasks/run")
    assert response.status_code == status.HTTP_200_OK
