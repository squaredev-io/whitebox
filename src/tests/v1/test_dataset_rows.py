from src.tests.v1.mock_data import dataset_rows_create_payload, dataset_rows_create_wrong_model_payload
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["dataset_rows"]["create"])
def test_dataset_row_create_many(client):
    response = client.post(
        "/v1/dataset_rows",
        json=list(map(lambda x: {**x, "model_id": state. model_multi["id"]}, dataset_rows_create_payload))
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["dataset_rows"]["create_model_doesn't_exist"])
def test_dataset_row_create_model_not_exist(client):
    response = client.post(
        "/v1/dataset_rows",
        json=(dataset_rows_create_wrong_model_payload),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.order(test_order_map["dataset_rows"]["get_model's_all"])
def test_dataset_row_get_models_all(client):
    response = client.get(f"/v1/{state.model_multi['id']}/dataset_rows")
    assert response.status_code == status.HTTP_200_OK
