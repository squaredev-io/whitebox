import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

model_integrity_metric_id = "1234567890"

@pytest.mark.order(test_order_map["model_integrity_metrics"]["get_model's_all"])
def test_model_integrity_metric_get_models_all(client):
    response = client.get(f"/v1/models/{state.model['id']}/model_integrity_metrics")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["model_integrity_metrics"]["get"])
def test_model_integrity_metric_get(client):
    response = client.get(f"/v1/model_integrity_metrics/{model_integrity_metric_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
