from datetime import datetime
from src.schemas.model import ModelType

register_payload = dict(
    email="mark@knight.com",
    password="pass",
)
login_payload = dict(username="mark@knight.com", password="pass")
client_update_payload = dict(password="pass1", email="mark@knight1.com")

user_create_payload = dict(name="User", email="user@yahoo.com", password="1234567890")
users_in_db = dict(amount=1)
user_update_payload = dict(
    name="Userius", email="user@yahoo.com", password="1234567890"
)

model_create_payload = dict(name="Model 1", type=ModelType.multi_class)
model_update_payload = dict(name="Model 2", type=ModelType.binary)


inference_create_payload = dict(
    timestamp=str(datetime.now()), inference={"a": 1, "b": 2}
)
inference_create_many_payload = list((
    dict(timestamp=str(datetime.now()), inference={"c": 3, "d": 4}),
    dict(timestamp=str(datetime.now()), inference={"e": 5, "f": 6})
))
