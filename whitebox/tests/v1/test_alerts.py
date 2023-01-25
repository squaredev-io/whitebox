import pytest
from whitebox import schemas
from whitebox.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("alerts_get"))
def test_alerts_get_model_all(client, api_key):
    response_all = client.get(
        f"/v1/alerts",
        headers={"api-key": api_key},
    )

    response_model_all = client.get(
        f"/v1/alerts?model_id={state.model_multi['id']}",
        headers={"api-key": api_key},
    )

    response_wrong_model = client.get(
        f"/v1/alerts?model_id=wrong_model_id",
        headers={"api-key": api_key},
    )

    assert response_all.status_code == status.HTTP_200_OK
    assert response_model_all.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND

    validated = [schemas.Alert(**m) for m in response_all.json()]
    validated = [schemas.Alert(**m) for m in response_model_all.json()]
