import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(
    get_order_number("model_integrity_metrics_get_model_multi_class_all")
)
def test_model_integrity_metric_get_model_multi_class_all(client):
    r = response = client.get(
        f"/v1/model-integrity-metrics?model_id={state.model_multi['id']}",
        headers={"api-key": state.api_key},
    )
    assert len(response.json()) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelIntegrityMetric(**m) for m in r.json()]


@pytest.mark.order(get_order_number("model_integrity_metrics_get_model_binary_all"))
def test_model_integrity_metric_get_model_binary_all(client):
    r = response = client.get(
        f"/v1/model-integrity-metrics?model_id={state.model_binary['id']}",
        headers={"api-key": state.api_key},
    )
    assert len(response.json()) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelIntegrityMetric(**m) for m in r.json()]
