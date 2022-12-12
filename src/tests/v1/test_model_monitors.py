import pytest
from src.tests.v1.mock_data import (
    model_monitor_accuracy_create_payload,
    model_monitor_f1_create_payload,
    model_monitor_data_drift_create_payload,
)
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("model_monitor_create"))
def test_model_monitor_create(client):
    accuracy_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_accuracy_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": state.api_key},
    )

    accuracy_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_f1_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": state.api_key},
    )

    accuracy_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_data_drift_create_payload,
            "model_id": state.model_binary["id"],
        },
        headers={"api-key": state.api_key},
    )

    assert accuracy_monitor.status_code == status.HTTP_201_CREATED
    validated = schemas.ModelMonitor(**accuracy_monitor.json())


@pytest.mark.order(get_order_number("model_monitors_get_model_all"))
def test_model_monitors_get_model_all(client):
    response = client.get(
        f"/v1/model-monitors?model_id={state.model_multi['id']}",
        headers={"api-key": state.api_key},
    )
    assert len(response.json()) == 2
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelMonitor(**m) for m in response.json()]
