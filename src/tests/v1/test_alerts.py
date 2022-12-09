import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("alerts_get_model_all"))
def test_alerts_get_model_all(client):
    response = client.get(
        f"/v1/alerts",
        headers={"api-key": state.api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    validated = [schemas.Alert(**m) for m in response.json()]
