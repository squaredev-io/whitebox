import pytest
from src.sdk import Whitebox
from src.tests.v1.conftest import get_order_number, state
from src.tests.v1.mock_data import model_multi_create_payload
import requests_mock


@pytest.mark.order(get_order_number("sdk"))
def test_sdk(client):
    wb = Whitebox(host=client.base_url, api_key=state.api_key)
    assert wb.host == client.base_url
    assert wb.api_key == state.api_key

    with requests_mock.Mocker() as m:
        m.post(
            url=f"{wb.host}/v1/models",
            json=model_multi_create_payload,
            headers={"api-key": wb.api_key},
        )

        r = wb.create_model(
            name=model_multi_create_payload["name"],
            description=model_multi_create_payload["description"],
            labels=model_multi_create_payload["labels"],
            features=model_multi_create_payload["features"],
            type=model_multi_create_payload["type"],
            probability=model_multi_create_payload["probability"],
            prediction=model_multi_create_payload["prediction"],
        )

        assert r == model_multi_create_payload
