from whitebox.tests.v1.mock_data import user_create_payload
import pytest
from whitebox import schemas
from whitebox.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("users_create"))
def test_user_create(client):
    response = client.post(
        "/v1/users",
        json={**user_create_payload, "api_key": state.api_key},
    )
    assert response.status_code == status.HTTP_201_CREATED
    state.user = response.json()
    assert response.json()["id"] is not None
    assert response.json()["username"] == user_create_payload["username"]
    validated = schemas.User(**response.json())


@pytest.mark.order(get_order_number("users_delete"))
def test_user_delete(client):
    response = client.delete(
        f"/v1/users/{state.user['id']}",
    )
    assert response.json() == {"status_code": str(status.HTTP_200_OK)}
