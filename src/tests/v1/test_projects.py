from src.tests.v1.mock_data import (
    project_create_payload,
    project_update_payload,
)
import pytest
from src.tests.v1.conftest import test_order_map, state
from fastapi import status


@pytest.mark.order(test_order_map["projects"]["create"])
def test_project_create(client):
    response = client.post(
        "/v1/projects",
        json={**project_create_payload, "user_id": state.client["id"]},
    )
    state.project = response.json()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(test_order_map["projects"]["get_all"])
def test_project_get_all(client):
    response = client.get(f"/v1/projects")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["projects"]["get"])
def test_project_get(client):
    response = client.get(f"/v1/projects/{state.project['id']}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["projects"]["update"])
def test_project_update(client):
    response = client.put(
        f"/v1/projects/{state.project['id']}", json=project_update_payload
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(test_order_map["projects"]["delete"])
def test_project_delete(client):
    response = client.delete(
        f"/v1/projects/{state.project['id']}",
    )
    assert response.status_code == status.HTTP_200_OK
