import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

performance_metric_id = "1234567890"


@pytest.mark.order(test_order_map["performance_metrics"]["get_model_multi_class_all"])
def test_performance_metric_get_model_multi_class_all(client):
    response = client.get(f"/v1/models/{state.model_multi['id']}/performance_metrics")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["performance_metrics"]["get_model_binary_all"])
def test_performance_metric_get_model_binary_all(client):
    response = client.get(f"/v1/models/{state.model_binary['id']}/performance_metrics")
    assert response.status_code == status.HTTP_200_OK
