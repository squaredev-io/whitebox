from src.tests.v1.mock_data import user_create_payload, user_update_payload
import pytest
from src.tests.v1.conftest import test_order_map
from . import test_apps

user_id = ""


@pytest.mark.order(test_order_map["users"]["create"])
def test_user_create(client, db):
    response = client.post(
        "/v1/users",
        json=user_create_payload,
        headers={"app-id": test_apps.app_id, "app-secret": test_apps.app_secret},
    )
    assert response.json()["id"] is not None
    assert response.json()["name"] == user_create_payload["name"]
    assert response.json()["app_id"] == test_apps.app_id
    assert response.json()["ext_id"] == user_create_payload["ext_id"]


@pytest.mark.order(test_order_map["users"]["update"])
def test_user_update(client, db):
    response = client.put(
        f"/v1/users/{user_create_payload['ext_id']}",
        json=user_update_payload,
        headers={"app-id": test_apps.app_id, "app-secret": test_apps.app_secret},
    )
    global user_id
    user_id = response.json()["ext_id"]
    assert response.json()["name"] == user_update_payload["name"]
    assert response.json()["app_id"] == test_apps.app_id
    assert response.json()["ext_id"] == user_update_payload["ext_id"]


@pytest.mark.order(test_order_map["users"]["get"])
def test_user_get(client, db):
    response = client.get(
        f"/v1/users/{user_update_payload['ext_id']}",
        headers={"app-id": test_apps.app_id, "app-secret": test_apps.app_secret},
    )
    assert response.json()["name"] == user_update_payload["name"]
    assert response.json()["app_id"] == test_apps.app_id
    assert response.json()["ext_id"] == user_update_payload["ext_id"]


@pytest.mark.order(test_order_map["users"]["delete"])
def test_user_delete(client, db):
    response = client.delete(
        f"/v1/users/{user_update_payload['ext_id']}",
        headers={"app-id": test_apps.app_id, "app-secret": test_apps.app_secret},
    )
    assert response.json() == str(200)
