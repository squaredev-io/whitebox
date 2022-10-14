import pytest
from src.tests.v1.conftest import test_order_map


@pytest.mark.order(test_order_map["health"])
def test_health(client, db, cron_client):
    # response = cron_client.post(
    #     "/v1/tasks/rdms_to_neo4j_intergration_pipeline/run",
    #     headers={"X-API-KEY": "1234567890"},
    # )

    response = client.get("/v1/health")
    assert response.json() == {"_": "Hello all possible worlds!", "status": 200}
