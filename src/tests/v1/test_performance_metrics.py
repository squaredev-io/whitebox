import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

performance_metric_id = "1234567890"

@pytest.mark.order(test_order_map["performance_metrics"]["get_model's_all"])
def test_performance_metric_get_models_all(client):
    response = client.get(f"/v1/models/{state.model['id']}/performance_metrics")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["performance_metrics"]["get"])
def test_performance_metric_get(client):
    response = client.get(f"/v1/performance_metrics/{performance_metric_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
