from src.tests.v1.mock_data import user_create_payload, users_in_db, user_update_payload
import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
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


@pytest.mark.order(get_order_number("users_get_all"))
def test_user_get_all(client):
    response = client.get(f"/v1/users")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == users_in_db["amount"]
    validated = [schemas.User(**m) for m in response.json()]


@pytest.mark.order(get_order_number("users_get"))
def test_user_get(client):
    response = client.get(f"/v1/users/{state.user['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_create_payload["username"]
    validated = schemas.User(**response.json())


@pytest.mark.order(get_order_number("users_update"))
def test_user_update(client):
    response = client.put(f"/v1/users/{state.user['id']}", json=user_update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_update_payload["username"]
    validated = schemas.User(**response.json())


@pytest.mark.order(get_order_number("users_delete"))
def test_user_delete(client):
    response = client.delete(
        f"/v1/users/{state.user['id']}",
    )
    assert response.json() == {"status_code": str(status.HTTP_200_OK)}
