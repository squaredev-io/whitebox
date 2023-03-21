import pytest
from whitebox.tests.v1.mock_data import (
    model_monitor_accuracy_create_payload,
    model_monitor_f1_create_payload,
    model_monitor_data_drift_create_payload,
    model_monitor_concept_drift_create_payload,
    model_monitor_precision_create_payload,
    model_monitor_r_square_create_payload,
    model_monitor_no_threshold_create_payload,
    model_monitor_no_feature_create_payload,
    model_monitor_feature_same_as_target_create_payload,
    model_monitor_feature_not_in_columns_create_payload,
    model_monitor_update_payload,
)
from whitebox import schemas
from whitebox.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("model_monitor_create"))
def test_model_monitor_create(client, api_key):
    accuracy_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_accuracy_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    f1_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_f1_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    data_drift_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_data_drift_create_payload,
            "model_id": state.model_binary["id"],
        },
        headers={"api-key": api_key},
    )

    concept_drift_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_concept_drift_create_payload,
            "model_id": state.model_binary["id"],
        },
        headers={"api-key": api_key},
    )

    precision_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_precision_create_payload,
            "model_id": state.model_binary["id"],
        },
        headers={"api-key": api_key},
    )

    r_square_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_r_square_create_payload,
            "model_id": state.model_regression["id"],
        },
        headers={"api-key": api_key},
    )

    wrong_model_monitor = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_r_square_create_payload,
            "model_id": "wrong_model_id",
        },
        headers={"api-key": api_key},
    )

    no_training_data = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_data_drift_create_payload,
            "model_id": state.model_multi_3["id"],
        },
        headers={"api-key": api_key},
    )

    no_threshold = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_no_threshold_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    no_feature = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_no_feature_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    feature_same_as_target = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_feature_same_as_target_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    feature_not_in_columns = client.post(
        "/v1/model-monitors",
        json={
            **model_monitor_feature_not_in_columns_create_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": api_key},
    )

    state.concept_drift_monitor = (
        concept_drift_monitor_json
    ) = concept_drift_monitor.json()

    assert concept_drift_monitor.status_code == status.HTTP_201_CREATED
    assert concept_drift_monitor_json["feature"] == "target"
    assert wrong_model_monitor.status_code == status.HTTP_404_NOT_FOUND
    assert no_threshold.status_code == status.HTTP_400_BAD_REQUEST
    assert no_feature.status_code == status.HTTP_400_BAD_REQUEST
    assert feature_same_as_target.status_code == status.HTTP_400_BAD_REQUEST
    assert feature_not_in_columns.status_code == status.HTTP_400_BAD_REQUEST
    assert no_training_data.status_code == status.HTTP_404_NOT_FOUND
    validated = schemas.ModelMonitor(**concept_drift_monitor_json)


@pytest.mark.order(get_order_number("model_monitors_get_model_all"))
def test_model_monitors_get_model_all(client, api_key):
    response_multi = client.get(
        f"/v1/model-monitors?model_id={state.model_multi['id']}",
        headers={"api-key": api_key},
    )
    response_all = client.get(
        f"/v1/model-monitors",
        headers={"api-key": api_key},
    )
    response_wrong_model = client.get(
        f"/v1/model-monitors?model_id=wrong_model_id",
        headers={"api-key": api_key},
    )

    assert len(response_multi.json()) == 2
    assert len(response_all.json()) == 6

    assert response_multi.status_code == status.HTTP_200_OK
    assert response_all.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = [schemas.ModelMonitor(**m) for m in response_multi.json()]
    validated = [schemas.ModelMonitor(**m) for m in response_all.json()]


@pytest.mark.order(get_order_number("model_monitor_update"))
def test_model_monitor_update(client, api_key):
    response = client.put(
        f"/v1/model-monitors/{state.concept_drift_monitor['id']}",
        json=model_monitor_update_payload,
        headers={"api-key": api_key},
    )
    response_wrong_model = client.put(
        f"/v1/model-monitors/wrong_model_id",
        json=model_monitor_update_payload,
        headers={"api-key": api_key},
    )

    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["lower_threshold"] == None
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = schemas.ModelMonitor(**response_json)


@pytest.mark.order(get_order_number("model_monitor_delete"))
def test_model_monitor_delete(client, api_key):
    response = client.delete(
        f"/v1/model-monitors/{state.concept_drift_monitor['id']}",
        headers={"api-key": api_key},
    )

    wrong_monitor_response = client.delete(
        f"/v1/model-monitors/wrong_model_monitor_id",
        headers={"api-key": api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    assert wrong_monitor_response.status_code == status.HTTP_404_NOT_FOUND
