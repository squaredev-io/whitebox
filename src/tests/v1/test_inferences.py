from src.tests.v1.mock_data import inference_create_payload, inference_create_many_payload
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["inferences"]["create"])
def test_inference_create(client):
    response = client.post(
        "/v1/inferences",
        json={**inference_create_payload, "model_id": state.model["id"]},
    )
    state.inference = response.json()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["inferences"]["create_many"])
def test_inference_create_many(client):
    response = client.post(
        "/v1/inferences/many",
        json=list(map(lambda x: {**x, "model_id": state.model["id"]}, inference_create_many_payload))
    )
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["inferences"]["get_all"])
def test_inference_get_all(client):
    response = client.get(f"/v1/inferences")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["inferences"]["get"])
def test_inference_get(client):
    response = client.get(f"/v1/inferences/{state.inference['id']}")
    assert response.status_code == status.HTTP_200_OK
