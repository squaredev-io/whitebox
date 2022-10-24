from src.tests.v1.mock_data import user_create_payload, users_in_db, user_update_payload
import pytest
from src.tests.v1.conftest import test_order_map
from fastapi import status

user_id = ""


@pytest.mark.order(test_order_map["users"]["create"])
def test_user_create(client):
    response = client.post(
        "/v1/users",
        json=user_create_payload,
    )
    global user_id
    user_id = response.json()["id"]
    assert response.json()["id"] is not None
    assert response.json()["name"] == user_create_payload["name"]
    assert response.json()["email"] == user_create_payload["email"]


@pytest.mark.order(test_order_map["users"]["get_all"])
def test_user_get_all(client):
    response = client.get(
        f"/v1/users"
    )
    assert len(response.json()) == users_in_db["amount"]


@pytest.mark.order(test_order_map["users"]["get"])
def test_user_get(client):
    response = client.get(
        f"/v1/users/{user_id}"
    )
    assert response.json()["name"] == user_create_payload["name"]
    assert response.json()["email"] == user_create_payload["email"]


@pytest.mark.order(test_order_map["users"]["update"])
def test_user_update(client):
    response = client.put(
        f"/v1/users/{user_id}",
        json=user_update_payload
    )
    assert response.json()["name"] == user_update_payload["name"]
    assert response.json()["email"] == user_update_payload["email"]


@pytest.mark.order(test_order_map["users"]["delete"])
def test_user_delete(client):
    response = client.delete(
        f"/v1/users/{user_id}",
    )
    assert response.json() == {"status_code": str(status.HTTP_200_OK)}
