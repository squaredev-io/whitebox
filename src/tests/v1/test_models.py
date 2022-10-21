from src.tests.v1.mock_data import (
    model_create_payload,
    model_update_payload,
)
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["models"]["create"])
def test_model_create(client):
    response = client.post(
        "/v1/models",
        json={**model_create_payload, "project_id": state.project["id"]},
    )

    state.model = response.json()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["models"]["get_all"])
def test_model_get_all(client):
    response = client.get(f"/v1/models")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["models"]["get"])
def test_model_get(client):
    response = client.get(f"/v1/models/{state.model['id']}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["models"]["update"])
def test_model_update(client):
    response = client.put(f"/v1/models/{state.model['id']}", json=model_update_payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["models"]["delete"])
def test_model_delete(client):
    response = client.delete(
        f"/v1/models/{state.model['id']}",
    )
    assert response.status_code == status.HTTP_200_OK
