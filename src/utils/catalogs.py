from src.schemas.app import App
from src.schemas.Catalog import Catalog


def catalog_belongs_to_app(app: App, catalog: Catalog) -> bool:
    if type(app) is not dict:
        app = app.__dict__
    if type(catalog) is not dict:
        catalog = catalog.__dict__
    return str(app["id"]) == str(catalog["app_id"])
