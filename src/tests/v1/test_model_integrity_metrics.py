import pytest
from src import schemas
from src.tests.v1.conftest import test_order_map, state
from fastapi import status

model_integrity_metric_id = "1234567890"


@pytest.mark.order(
    test_order_map["model_integrity_metrics"]["get_model_multi_class_all"]
)
def test_model_integrity_metric_get_model_multi_class_all(client):
    r = response = client.get(
        f"/v1/models/{state.model_multi['id']}/model_integrity_metrics"
    )
    assert len(response.json()) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelIntegrityMetric(**m) for m in r.json()]


@pytest.mark.order(test_order_map["model_integrity_metrics"]["get_model_binary_all"])
def test_model_integrity_metric_get_model_binary_all(client):
    r = response = client.get(
        f"/v1/models/{state.model_binary['id']}/model_integrity_metrics"
    )
    assert len(response.json()) == 1
    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.ModelIntegrityMetric(**m) for m in r.json()]
