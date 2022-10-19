import requests
from fastapi.testclient import TestClient

from src.simulator import simulator_app
from src.core.settings import get_settings

agent = TestClient(simulator_app)


def get_agent():
    if get_settings().ENV not in ["dev", "test", "ci"]:
        return requests
    return agent
