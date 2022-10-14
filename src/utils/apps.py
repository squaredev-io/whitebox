from src.schemas.app import App
from src.schemas.Client import Client


def is_app_owner(app: App, current_client: Client) -> bool:
    if type(app) is not dict:
        app = app.__dict__
    if type(current_client) is not dict:
        current_client = current_client.__dict__
    return str(app["client_id"]) == str(current_client["id"])
