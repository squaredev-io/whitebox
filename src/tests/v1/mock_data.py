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

model_create_payload = dict(
    name="Model 1",
    type=ModelType.multi_class,
    features={"feature": 1},
    predictions={"prediction": 1},
    labels={"label": 1}
)
model_update_payload = dict(
    name="Model 2",
    type=ModelType.binary,
    features={"feature": 2},
    predictions={"prediction": 2},
    labels={"label": 2}
)


inference_create_payload = dict(
    timestamp=str(datetime.now()),
    features={"feature": 1},
    raw={"raw": 1},
    prediction={"prediction": 1},
    actuals={"actual": 1}
)

inference_create_many_payload = list((
    dict(
        timestamp=str(datetime.now()),
        features={"feature": 2},
        raw={"raw": 2},
        prediction={"prediction": 2},
        actuals={"actual": 2}
    ),
    dict(
        timestamp=str(datetime.now()),
        features={"feature": 3},
        raw={"raw": 3},
        prediction={"prediction": 3},
        actuals={"actual": 3}
    )
))
