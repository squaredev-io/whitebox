import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("drifting_metrics_get_model_multi_class_all"))
def test_drifting_metric_get_model_multi_class_all(client):
    response = client.get(
        f"/v1/drifting-metrics?model_id={state.model_multi['id']}",
        headers={"api-key": state.api_key},
    )
    r = response.json()
    assert len(r) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.DriftingMetric(**m) for m in r]


@pytest.mark.order(get_order_number("drifting_metrics_get_model_binary_all"))
def test_drifting_metric_get_model_binary_all(client):
    response = client.get(
        f"/v1/drifting-metrics?model_id={state.model_binary['id']}",
        headers={"api-key": state.api_key},
    )
    r = response.json()
    assert len(r) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.DriftingMetric(**m) for m in r]
