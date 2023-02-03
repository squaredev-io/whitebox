from whitebox.tests.v1.mock_data import (
    model_binary_create_payload,
    model_multi_create_payload,
    model_multi_2_create_payload,
    model_multi_3_create_payload,
    model_regression_create_payload,
    model_update_payload,
)
import pytest
from whitebox import schemas
from whitebox.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("models_create"))
def test_model_create(client, api_key):
    response_binary = client.post(
        "/v1/models",
        json={**model_binary_create_payload},
        headers={"api-key": api_key},
    )

    response_multi = client.post(
        "/v1/models",
        json={**model_multi_create_payload},
        headers={"api-key": api_key},
    )

    response_multi_2 = client.post(
        "/v1/models",
        json={**model_multi_2_create_payload},
        headers={"api-key": api_key},
    )

    response_multi_3 = client.post(
        "/v1/models",
        json={**model_multi_3_create_payload},
        headers={"api-key": api_key},
    )

    response_regression = client.post(
        "/v1/models",
        json={**model_regression_create_payload},
        headers={"api-key": api_key},
    )

    state.model_binary = response_binary.json()
    state.model_multi = response_multi.json()
    state.model_multi_2 = response_multi_2.json()
    state.model_multi_3 = response_multi_3.json()
    state.model_regression = response_regression.json()

    assert response_binary.status_code == status.HTTP_201_CREATED
    assert response_multi.status_code == status.HTTP_201_CREATED
    assert response_multi_2.status_code == status.HTTP_201_CREATED
    assert response_multi_3.status_code == status.HTTP_201_CREATED
    assert response_regression.status_code == status.HTTP_201_CREATED

    validated = schemas.Model(**response_binary.json())
    validated = schemas.Model(**response_multi.json())
    validated = schemas.Model(**response_multi_2.json())
    validated = schemas.Model(**response_multi_3.json())
    validated = schemas.Model(**response_regression.json())


@pytest.mark.order(get_order_number("models_get_all"))
def test_model_get_all(client, api_key):
    response = client.get(f"/v1/models", headers={"api-key": api_key})
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.Model(**m) for m in response.json()]


@pytest.mark.order(get_order_number("models_get"))
def test_model_get(client, api_key):
    response = client.get(
        f"/v1/models/{state.model_multi['id']}", headers={"api-key": api_key}
    )
    response_wrong_model = client.get(
        f"/v1/models/wrong_model_id", headers={"api-key": api_key}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = schemas.Model(**response.json())


@pytest.mark.order(get_order_number("models_update"))
def test_model_update(client, api_key):
    response = client.put(
        f"/v1/models/{state.model_multi['id']}",
        json=model_update_payload,
        headers={"api-key": api_key},
    )
    response_wrong_model = client.put(
        f"/v1/models/wrong_model_id",
        json=model_update_payload,
        headers={"api-key": api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = schemas.Model(**response.json())


@pytest.mark.order(get_order_number("models_delete"))
def test_model_delete(client, api_key):
    response_binary = client.delete(
        f"/v1/models/{state.model_binary['id']}", headers={"api-key": api_key}
    )
    response_multi = client.delete(
        f"/v1/models/{state.model_multi['id']}", headers={"api-key": api_key}
    )
    response_multi_2 = client.delete(
        f"/v1/models/{state.model_multi_2['id']}", headers={"api-key": api_key}
    )
    response_multi_3 = client.delete(
        f"/v1/models/{state.model_multi_3['id']}", headers={"api-key": api_key}
    )
    response_regression = client.delete(
        f"/v1/models/{state.model_regression['id']}", headers={"api-key": api_key}
    )
    response_no_model = client.delete(
        f"/v1/models/{state.model_binary['id']}", headers={"api-key": api_key}
    )

    assert response_binary.status_code == status.HTTP_200_OK
    assert response_multi.status_code == status.HTTP_200_OK
    assert response_multi_2.status_code == status.HTTP_200_OK
    assert response_multi_3.status_code == status.HTTP_200_OK
    assert response_regression.status_code == status.HTTP_200_OK
    assert response_no_model.status_code == status.HTTP_404_NOT_FOUND
