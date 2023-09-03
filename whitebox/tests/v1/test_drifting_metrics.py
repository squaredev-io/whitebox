import pytest
from whitebox import schemas
from whitebox.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("drifting_metrics_get_model_all"))
def test_drifting_metric_get_model_all(client, api_key):
    response_multi = client.get(
        f"/v1/drifting-metrics?model_id={state.model_multi['id']}",
        headers={"api-key": api_key},
    )

    response_binary = client.get(
        f"/v1/drifting-metrics?model_id={state.model_binary['id']}",
        headers={"api-key": api_key},
    )
    response_wrong_model = client.get(
        f"/v1/drifting-metrics?model_id=wrong_model_id",
        headers={"api-key": api_key},
    )

    response_binary_json = response_binary.json()
    response_multi_json = response_multi.json()

    assert len(response_multi_json) == 1
    assert len(response_binary_json) == 1

    assert response_multi_json[0]["timestamp"] == "2023-03-06T12:15:00+00:00"
    assert response_binary_json[0]["timestamp"] == "2023-03-07T00:00:00+00:00"

    assert response_multi.status_code == status.HTTP_200_OK
    assert response_binary.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = [schemas.DriftingMetric(**m) for m in response_multi_json]
    validated = [schemas.DriftingMetric(**m) for m in response_binary_json]


@pytest.mark.order(get_order_number("drifting_metrics_get_binary_model_after_x_time"))
def test_drifting_metrics_get_binary_model_after_x_time(client, api_key):
    response_binary = client.get(
        f"/v1/drifting-metrics?model_id={state.model_binary['id']}",
        headers={"api-key": api_key},
    )

    response_binary_json = response_binary.json()

    assert len(response_binary_json) == 1

    assert response_binary_json[0]["timestamp"] == "2023-03-07T00:00:00+00:00"

    assert response_binary.status_code == status.HTTP_200_OK

    validated = [schemas.DriftingMetric(**m) for m in response_binary_json]
