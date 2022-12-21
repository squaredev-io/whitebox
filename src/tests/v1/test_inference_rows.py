from src.tests.v1.mock_data import (
    inference_row_create_single_row_payload,
    inference_row_create_many_binary_payload,
    inference_row_create_many_multi_payload,
    inference_row_create_many_multi_no_actual_payload,
    inference_row_create_many_multi_mixed_actuals_payload,
)
import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("inference_rows_create"))
def test_inference_row_create(client):
    response = client.post(
        "/v1/inference-rows",
        json={
            **inference_row_create_single_row_payload,
            "model_id": state.model_multi["id"],
        },
        headers={"api-key": state.api_key},
    )
    state.inference_row_multi = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    validated = schemas.InferenceRow(**response.json())


@pytest.mark.order(get_order_number("inference_rows_create_many"))
def test_inference_row_create_many(client):
    response_binary = client.post(
        "/v1/inference-rows/batch",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_binary["id"]},
                inference_row_create_many_binary_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    state.inference_row_binary = response_binary.json()[0]

    response_multi = client.post(
        "/v1/inference-rows/batch",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_multi["id"]},
                inference_row_create_many_multi_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    response_multi_2 = client.post(
        "/v1/inference-rows/batch",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_multi_2["id"]},
                inference_row_create_many_multi_no_actual_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    response_multi_3 = client.post(
        "/v1/inference-rows/batch",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_multi_3["id"]},
                inference_row_create_many_multi_mixed_actuals_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    assert response_binary.status_code == status.HTTP_201_CREATED
    assert response_multi.status_code == status.HTTP_201_CREATED
    validated = [schemas.InferenceRow(**m) for m in response_binary.json()]
    validated = [schemas.InferenceRow(**m) for m in response_multi.json()]
    validated = [schemas.InferenceRow(**m) for m in response_multi_2.json()]
    validated = [schemas.InferenceRow(**m) for m in response_multi_3.json()]


@pytest.mark.order(get_order_number("inference_rows_get_model's_all"))
def test_inference_row_get_models_all(client):
    response_multi = client.get(
        f"/v1/inference-rows?model_id={state.model_multi['id']}",
        headers={"api-key": state.api_key},
    )
    response_binary = client.get(
        f"/v1/inference-rows?model_id={state.model_binary['id']}",
        headers={"api-key": state.api_key},
    )
    response_wrong_model = client.get(
        f"/v1/inference-rows?model_id=wrong_model_id",
        headers={"api-key": state.api_key},
    )
    assert response_multi.status_code == status.HTTP_200_OK
    assert response_binary.status_code == status.HTTP_200_OK
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND
    validated = [schemas.InferenceRow(**m) for m in response_multi.json()]
    validated = [schemas.InferenceRow(**m) for m in response_binary.json()]


@pytest.mark.order(get_order_number("inference_rows_get"))
def test_inference_row_get(client):
    response = client.get(
        f"/v1/inference-rows/{state.inference_row_multi['id']}",
        headers={"api-key": state.api_key},
    )
    response_wrong_inference = client.get(
        f"/v1/inference-rows/wrong_inference_id",
        headers={"api-key": state.api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response_wrong_inference.status_code == status.HTTP_404_NOT_FOUND
    validated = schemas.InferenceRow(**response.json())


@pytest.mark.order(get_order_number("inference_rows_xai"))
def test_inference_row_xai(client):
    response = client.get(
        f"/v1/inference-rows/{state.inference_row_binary['id']}/xai",
        headers={"api-key": state.api_key},
    )

    response_wrong_inference = client.get(
        f"/v1/inference-rows/wrong_inference_id/xai",
        headers={"api-key": state.api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response_wrong_inference.status_code == status.HTTP_404_NOT_FOUND
