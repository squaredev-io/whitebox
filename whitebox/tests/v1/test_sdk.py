import pandas as pd
import pytest
from whitebox.schemas.modelMonitor import AlertSeverity, MonitorMetrics, MonitorStatus
from whitebox.sdk import Whitebox
from whitebox.tests.v1.conftest import get_order_number, state, state_sdk
from whitebox.tests.v1.mock_data import (
    model_multi_create_payload,
    timestamps,
    mixed_actuals,
    inference_row_xai_payload,
    alert_payload,
    drifting_metrics_report_payload,
    descriptive_statistics_report_payload,
    performance_metrics_report_payload,
)
import requests_mock
from fastapi import status


@pytest.mark.order(get_order_number("sdk_init"))
def test_sdk_init(client, api_key):
    wb = Whitebox(host=client.base_url, api_key=api_key)
    assert wb.host == client.base_url
    assert wb.api_key == api_key
    state_sdk.wb = wb


@pytest.mark.order(get_order_number("sdk_create_model"))
def test_sdk_create_model(client):
    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/models",
            json=model_multi_create_payload,
            headers={"api-key": state_sdk.wb.api_key},
        )

        model = state_sdk.wb.create_model(
            name=model_multi_create_payload["name"],
            description=model_multi_create_payload["description"],
            labels=model_multi_create_payload["labels"],
            type=model_multi_create_payload["type"],
            target_column=model_multi_create_payload["target_column"],
            granularity=model_multi_create_payload["granularity"],
        )

        assert model == model_multi_create_payload


@pytest.mark.order(get_order_number("sdk_get_model"))
def test_sdk_get_model(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_model(model_id=mock_model_id)

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=state.model_multi,
        )

        model = state_sdk.wb.get_model(model_id=mock_model_id)

        assert model == state.model_multi


@pytest.mark.order(get_order_number("sdk_delete_model"))
def test_sdk_delete_model(client):
    mock_model_id = "mock_model_id"

    with requests_mock.Mocker() as m:
        m.delete(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_200_OK,
        )

        happy_result = state_sdk.wb.delete_model(model_id=mock_model_id)
        assert happy_result == True

        m.delete(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        sad_result = state_sdk.wb.delete_model(model_id=mock_model_id)
        assert sad_result == False


@pytest.mark.order(get_order_number("sdk_log_training_dataset"))
def test_sdk_log_training_dataset(client):
    mock_model_id = "mock_model_id"
    df = pd.read_csv("whitebox/analytics/data/testing/classification_test_data.csv")

    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/dataset-rows",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_201_CREATED,
        )

        happy_result = state_sdk.wb.log_training_dataset(
            model_id=mock_model_id, processed=df, non_processed=df
        )
        assert happy_result == True

        m.post(
            url=f"{state_sdk.wb.host}/v1/dataset-rows",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        sad_result = state_sdk.wb.log_training_dataset(
            model_id=mock_model_id, processed=df, non_processed=df
        )
        assert sad_result == False

    # drop a row in df to test the dataframe length error handling
    df2 = df.drop(df.index[0])
    with pytest.raises(Exception) as e_info:
        state_sdk.wb.log_inferences(
            model_id=mock_model_id, processed=df, non_processed=df2
        )


@pytest.mark.order(get_order_number("sdk_log_inferences"))
def test_sdk_log_inferences(client):
    mock_model_id = "mock_model_id"
    df = pd.read_csv("whitebox/analytics/data/testing/classification_test_data.csv")

    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/inference-rows/batch",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_201_CREATED,
        )

        happy_result = state_sdk.wb.log_inferences(
            model_id=mock_model_id,
            processed=df,
            non_processed=df,
            timestamps=timestamps,
            actuals=mixed_actuals,
        )
        assert happy_result == True

        m.post(
            url=f"{state_sdk.wb.host}/v1/inference-rows/batch",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        sad_result = state_sdk.wb.log_inferences(
            model_id=mock_model_id,
            processed=df,
            non_processed=df,
            timestamps=timestamps,
        )
        assert sad_result == False

    # drop a row in df to test the dataframe length error handling
    df2 = df.drop(df.index[0])
    with pytest.raises(Exception) as e_info:
        state_sdk.wb.log_inferences(
            model_id=mock_model_id,
            processed=df,
            non_processed=df2,
            timestamps=timestamps,
            actuals=mixed_actuals,
        )


@pytest.mark.order(get_order_number("sdk_create_model_monitor"))
def test_sdk_create_model_monitor(client):
    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/model-monitors",
            json=model_multi_create_payload,
            headers={"api-key": state_sdk.wb.api_key},
        )

        model_monitor = state_sdk.wb.create_model_monitor(
            model_id="mock_model_id",
            name="test",
            status=MonitorStatus.active,
            metric=MonitorMetrics.accuracy,
            feature="feature1",
            lower_threshold=0.7,
            severity=AlertSeverity.high,
            email="jaclie.chan@chinamail.io",
        )

        assert model_monitor is not None


@pytest.mark.order(get_order_number("sdk_get_alerts"))
def test_sdk_get_alerts(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/alerts?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_alerts(model_id=mock_model_id)

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/alerts?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=alert_payload,
        )

        alert = state_sdk.wb.get_alerts(model_id=mock_model_id)

        assert alert == alert_payload


@pytest.mark.order(get_order_number("sdk_get_drifting_metrics"))
def test_sdk_get_drifting_metrics(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/drifting-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_drifting_metrics(model_id=mock_model_id)

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/drifting-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=drifting_metrics_report_payload,
        )

        drifting_report = state_sdk.wb.get_drifting_metrics(model_id=mock_model_id)

        assert drifting_report == drifting_metrics_report_payload


@pytest.mark.order(get_order_number("sdk_get_descriptive_statistics"))
def test_sdk_get_descriptive_statistics(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/model-integrity-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_descriptive_statistics(
            model_id=mock_model_id
        )

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/model-integrity-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=descriptive_statistics_report_payload,
        )

        descriptive_report = state_sdk.wb.get_descriptive_statistics(
            model_id=mock_model_id
        )

        assert descriptive_report == descriptive_statistics_report_payload


@pytest.mark.order(get_order_number("sdk_get_performance_metrics"))
def test_sdk_get_performance_metrics(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/performance-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_performance_metrics(model_id=mock_model_id)

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/performance-metrics?model_id={mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=performance_metrics_report_payload,
        )

        performance_report = state_sdk.wb.get_performance_metrics(
            model_id=mock_model_id
        )

        assert performance_report == performance_metrics_report_payload


@pytest.mark.order(get_order_number("sdk_get_xai_row"))
def test_sdk_get_xai_row(client):
    mock_inference_id = "mock_inference_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/inference-rows/{mock_inference_id}/xai",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        not_found_result = state_sdk.wb.get_xai_row(inference_row_id=mock_inference_id)

        assert not_found_result == None

        m.get(
            url=f"{state_sdk.wb.host}/v1/inference-rows/{mock_inference_id}/xai",
            headers={"api-key": state_sdk.wb.api_key},
            json=inference_row_xai_payload,
        )

        xai = state_sdk.wb.get_xai_row(inference_row_id=mock_inference_id)

        assert xai == inference_row_xai_payload
