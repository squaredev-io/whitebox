import pytest
from whitebox.tests.v1.conftest import get_order_number
from fastapi import status


@pytest.mark.order(get_order_number("cron_tasks_run_no_models"))
def test_cron_tasks_no_models(client):
    response = client.post("/v1/cron-tasks/run")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(get_order_number("cron_tasks_run_no_inference"))
def test_cron_tasks_no_inference(client):
    response = client.post("/v1/cron-tasks/run")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(get_order_number("cron_tasks_run_ok"))
def test_cron_tasks_ok(client):
    response = client.post("/v1/cron-tasks/run")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(get_order_number("cron_tasks_run_after_x_time"))
def test_cron_tasks_run_after_x_time(client):
    response = client.post("/v1/cron-tasks/run")
    assert response.status_code == status.HTTP_200_OK
