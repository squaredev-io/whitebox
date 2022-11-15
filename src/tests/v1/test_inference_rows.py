from src.tests.v1.mock_data import (
    inference_row_create_payload,
    inference_row_create_many_binary_payload,
    inference_row_create_many_multi_payload
)
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["inference_rows"]["create"])
def test_inference_row_create(client):
    response = client.post(
        "/v1/inference_rows",
        json={**inference_row_create_payload, "model_id": state.model_multi["id"]},
    )
    state.inference_row = response.json()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["inference_rows"]["create_many"])
def test_inference_row_create_many(client):
    response_binary = client.post(
        "/v1/inference_rows/many",
        json=list(map(lambda x: {**x, "model_id": state.model_binary["id"]}, inference_row_create_many_binary_payload))
    )

    response_multi = client.post(
        "/v1/inference_rows/many",
        json=list(map(lambda x: {**x, "model_id": state.model_multi["id"]}, inference_row_create_many_multi_payload))
    )

    assert response_binary.status_code == status.HTTP_201_CREATED
    assert response_multi.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["inference_rows"]["get_model's_all"])
def test_inference_row_get_models_all(client):
    response = client.get(f"/v1/models/{state.model_multi['id']}/inference_rows")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["inference_rows"]["get"])
def test_inference_row_get(client):
    response = client.get(f"/v1/inference_rows/{state.inference_row['id']}")
    assert response.status_code == status.HTTP_200_OK
