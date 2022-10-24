from src.schemas.user import User


def user_belongs_to_app(app: App, user: User) -> bool:
    if type(app) is not dict:
        app = app
    if type(user) is not dict:
        user = user
    return str(app["id"]) == str(user["app_id"])
