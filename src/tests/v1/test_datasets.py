from src.tests.v1.mock_data import dataset_create_payload
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["datasets"]["create"])
def test_dataset_create(client):
    response = client.post(
        "/v1/datasets/metadata",
        json={**dataset_create_payload, "user_id": state.user["id"]},
    )

    state.dataset = response.json()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["datasets"]["get"])
def test_dataset_get(client):
    response = client.get(f"/v1/datasets/{state.dataset['id']}")
    assert response.status_code == status.HTTP_200_OK