from src.tests.v1.mock_data import app_create_payload, app_update_payload
import pytest
from src.tests.v1.conftest import test_order_map
from . import test_auth, test_client

app_id = ""
app_secret = ""


@pytest.mark.order(test_order_map["apps"]["create"])
def test_app_create(client, db):
    response = client.post(
        "/v1/apps",
        json=app_create_payload,
        headers={"Authorization": test_auth.access_token},
    )
    global app_id
    global app_secret
    app_id = response.json()["id"]
    app_secret = response.json()["secret"]
    assert response.json()["name"] == app_create_payload["name"]
    assert response.json()["client_id"] == test_client.client_id
    assert len(response.json()["secret"]) == 32


@pytest.mark.order(test_order_map["apps"]["get"])
def test_app_get(client, db):
    response = client.get(
        f"/v1/apps/{app_id}", headers={"Authorization": test_auth.access_token}
    )
    assert response.json()["id"] == app_id
    assert response.json()["name"] == app_create_payload["name"]
    assert response.json()["client_id"] == test_client.client_id
    assert len(response.json()["secret"]) == 32


@pytest.mark.order(test_order_map["apps"]["update"])
def test_app_update(client, db):
    response = client.put(
        f"/v1/apps/{app_id}",
        json=app_update_payload,
        headers={"Authorization": test_auth.access_token},
    )
    assert response.json()["name"] == app_update_payload["name"]


@pytest.mark.order(test_order_map["apps"]["delete"])
def test_app_delete(client, db):
    response = client.delete(
        f"/v1/apps/{app_id}", headers={"Authorization": test_auth.access_token}
    )
    assert response.json() == str(200)


@pytest.mark.order(test_order_map["apps"]["get_upon_delete"])
def test_app_get(client, db):
    response = client.get(
        f"/v1/apps/{app_id}", headers={"Authorization": test_auth.access_token}
    )
    assert response.json() == {"status_code": 404, "error": "App not found"}
