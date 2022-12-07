import pytest
from src.tests.v1.mock_data import model_monitor_create_payload
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("model_monitor_create"))
def test_model_monitor_create(client):
    response = client.post(
        "/v1/model-monitors",
        json={**model_monitor_create_payload, "model_id": state.model_multi["id"]},
        headers={"api-key": state.api_key},
    )

    assert response.status_code == status.HTTP_201_CREATED
    validated = schemas.ModelMonitor(**response.json())


@pytest.mark.order(get_order_number("model_monitors_get_model_all"))
def test_model_monitors_get_model_all(client):
    r = response = client.get(
        f"/v1/models/{state.model_multi['id']}/model-monitors",
        headers={"api-key": state.api_key},
    )
    assert len(response.json()) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelMonitor(**m) for m in r.json()]
