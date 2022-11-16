import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status

performance_metric_id = "1234567890"


@pytest.mark.order(get_order_number("performance_metrics_get_model_multi_class_all"))
def test_performance_metric_get_model_multi_class_all(client):
    response = client.get(f"/v1/models/{state.model_multi['id']}/performance_metrics")
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.MultiClassificationMetrics(**m) for m in response.json()]


@pytest.mark.order(get_order_number("performance_metrics_get_model_binary_all"))
def test_performance_metric_get_model_binary_all(client):
    response = client.get(f"/v1/models/{state.model_binary['id']}/performance_metrics")
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.BinaryClassificationMetrics(**m) for m in response.json()]
