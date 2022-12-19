import pytest
from src.tests.v1.conftest import get_order_number
from fastapi import status


@pytest.mark.order(get_order_number("models_no_api_key"))
def test_model_no_api_key(client):
    response = client.get("/v1/models")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.order(get_order_number("models_wrong_api_key"))
def test_model_wrong_api_key(client):
    response = client.get(
        "/v1/models",
        headers={"api-key": "1234567890"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
