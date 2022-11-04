from src.tests.v1.mock_data import dataset_rows_create_payload, dataset_rows_create_wrong_dataset_payload
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["dataset_rows"]["create"])
def test_dataset_row_create_many(client):
    response = client.post(
        "/v1/datasets/rows",
        json=list(map(lambda x: {**x, "dataset_id": state.dataset["id"]}, dataset_rows_create_payload))
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["dataset_rows"]["create_dataset_doesn't_exist"])
def test_dataset_row_create_dataset_not_exist(client):
    response = client.post(
        "/v1/datasets/rows",
        json=(dataset_rows_create_wrong_dataset_payload),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.order(test_order_map["dataset_rows"]["get_dataset's_all"])
def test_dataset_row_get_datasets_all(client):
    response = client.get(f"/v1/datasets/{state.dataset['id']}/rows")
    assert response.status_code == status.HTTP_200_OK
