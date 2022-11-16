from src.tests.v1.mock_data import (
    model_binary_create_payload,
    model_multi_create_payload,
    model_update_payload,
)
import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("models_create"))
def test_model_create(client):
    response_binary = client.post(
        "/v1/models",
        json={**model_binary_create_payload, "user_id": state.user["id"]},
    )

    response_multi = client.post(
        "/v1/models",
        json={**model_multi_create_payload, "user_id": state.user["id"]},
    )

    state.model_binary = response_binary.json()
    state.model_multi = response_multi.json()
    assert response_binary.status_code == status.HTTP_201_CREATED
    assert response_multi.status_code == status.HTTP_201_CREATED
    validated = schemas.Model(**response_binary.json())
    validated = schemas.Model(**response_multi.json())


@pytest.mark.order(get_order_number("models_get_all"))
def test_model_get_all(client):
    response = client.get(f"/v1/models")
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.Model(**m) for m in response.json()]


@pytest.mark.order(get_order_number("models_get"))
def test_model_get(client):
    response = client.get(f"/v1/models/{state.model_multi['id']}")
    assert response.status_code == status.HTTP_200_OK
    validated = schemas.Model(**response.json())


@pytest.mark.order(get_order_number("models_update"))
def test_model_update(client):
    response = client.put(
        f"/v1/models/{state.model_multi['id']}", json=model_update_payload
    )
    assert response.status_code == status.HTTP_200_OK
    validated = schemas.Model(**response.json())


@pytest.mark.order(get_order_number("models_delete"))
def test_model_delete(client):
    response = client.delete(
        f"/v1/models/{state.model_multi['id']}",
    )
    assert response.status_code == status.HTTP_200_OK
