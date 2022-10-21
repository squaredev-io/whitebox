from src.schemas.user import User


def user_belongs_to_app(app: App, user: User) -> bool:
    if type(app) is not dict:
        app = app.__dict__
    if type(user) is not dict:
        user = user.__dict__
    return str(app["id"]) == str(user["app_id"])
