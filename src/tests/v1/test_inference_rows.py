from src.tests.v1.mock_data import (
    inference_row_create_payload,
    inference_row_create_many_binary_payload,
    inference_row_create_many_multi_payload,
)
import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("inference_rows_create"))
def test_inference_row_create(client):
    response = client.post(
        "/v1/inference_rows",
        json={**inference_row_create_payload, "model_id": state.model_multi["id"]},
        headers={"api-key": state.api_key},
    )
    state.inference_row = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    validated = schemas.InferenceRow(**response.json())


@pytest.mark.order(get_order_number("inference_rows_create_many"))
def test_inference_row_create_many(client):
    response_binary = client.post(
        "/v1/inference_rows/many",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_binary["id"]},
                inference_row_create_many_binary_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    response_multi = client.post(
        "/v1/inference_rows/many",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_multi["id"]},
                inference_row_create_many_multi_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    assert response_binary.status_code == status.HTTP_201_CREATED
    assert response_multi.status_code == status.HTTP_201_CREATED
    validated = [schemas.InferenceRow(**m) for m in response_multi.json()]
    validated = [schemas.InferenceRow(**m) for m in response_binary.json()]


@pytest.mark.order(get_order_number("inference_rows_get_model's_all"))
def test_inference_row_get_models_all(client):
    response_multi = client.get(
        f"/v1/models/{state.model_multi['id']}/inference_rows",
        headers={"api-key": state.api_key},
    )
    response_binary = client.get(
        f"/v1/models/{state.model_binary['id']}/inference_rows",
        headers={"api-key": state.api_key},
    )
    assert response_multi.status_code == status.HTTP_200_OK
    assert response_binary.status_code == status.HTTP_200_OK
    validated = [schemas.InferenceRow(**m) for m in response_multi.json()]
    validated = [schemas.InferenceRow(**m) for m in response_binary.json()]


@pytest.mark.order(get_order_number("inference_rows_get"))
def test_inference_row_get(client):
    response = client.get(
        f"/v1/inference_rows/{state.inference_row['id']}",
        headers={"api-key": state.api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    validated = schemas.InferenceRow(**response.json())
