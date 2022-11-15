import pytest
from src.schemas.driftingMetric import DriftingMetric
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

drifting_metric_id = "1234567890"


@pytest.mark.order(test_order_map["drifting_metrics"]["get_model_multi_all"])
def test_drifting_metric_get_model_multi_class_all(client):
    response = client.get(f"/v1/models/{state.model_multi['id']}/drifting_metrics")
    r = response.json()
    assert len(r) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [DriftingMetric(**m) for m in r]


@pytest.mark.order(test_order_map["drifting_metrics"]["get_model_binary_all"])
def test_drifting_metric_get_model_binary_all(client):
    response = client.get(f"/v1/models/{state.model_binary['id']}/drifting_metrics")
    r = response.json()
    assert len(r) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [DriftingMetric(**m) for m in r]
