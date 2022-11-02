import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

drifting_metric_id = "1234567890"

@pytest.mark.order(test_order_map["drifting_metrics"]["get_model's_all"])
def test_drifting_metric_get_models_all(client):
    response = client.get(f"/v1/models/{state.model['id']}/drifting_metrics")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["drifting_metrics"]["get"])
def test_drifting_metric_get(client):
    response = client.get(f"/v1/drifting_metrics/{drifting_metric_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
