import pandas as pd
import pytest
from src.sdk import Whitebox
from src.tests.v1.conftest import get_order_number, state, state_sdk
from src.tests.v1.mock_data import model_multi_create_payload
import requests_mock
from fastapi import status


@pytest.mark.order(get_order_number("sdk_init"))
def test_sdk_init(client):
    wb = Whitebox(host=client.base_url, api_key=state.api_key)
    assert wb.host == client.base_url
    assert wb.api_key == state.api_key
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
            features=model_multi_create_payload["features"],
            type=model_multi_create_payload["type"],
            probability=model_multi_create_payload["probability"],
            prediction=model_multi_create_payload["prediction"],
        )

        assert model == model_multi_create_payload


@pytest.mark.order(get_order_number("sdk_get_model"))
def test_sdk_get_model(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
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
    df = pd.read_csv("src/analytics/data/testing/classification_test_data.csv")

    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/dataset-rows",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_200_OK,
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


@pytest.mark.order(get_order_number("sdk_log_inferences"))
def test_sdk_log_inferences(client):
    mock_model_id = "mock_model_id"
    df = pd.read_csv("src/analytics/data/testing/classification_test_data.csv")

    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/inference-rows/batch",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_200_OK,
        )

        happy_result = state_sdk.wb.log_inferences(
            model_id=mock_model_id, processed=df, non_processed=df
        )
        assert happy_result == True

        m.post(
            url=f"{state_sdk.wb.host}/v1/inference-rows/batch",
            headers={"api-key": state_sdk.wb.api_key},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        sad_result = state_sdk.wb.log_inferences(
            model_id=mock_model_id, processed=df, non_processed=df
        )
        assert sad_result == False
