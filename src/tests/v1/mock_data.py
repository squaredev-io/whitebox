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
    description="Model 1 description",
    type=ModelType.multi_class,
    features={"feature_1": "boolean", "feature_2": "categorical"},
    labels={"age": 1, "gender": 2},
    prediction="predicted",
    probability="zero"
)
model_update_payload = dict(
    name="Model 2",
    type=ModelType.binary,
    description="Model 2 description",
)

dataset_create_payload = dict(
    name="Dataset 1",
    target="target"
)

dataset_wrong_user_create_payload = dict(
    user_id="1234567890",
    name="Dataset 2",
    target="target"
)

dataset_rows_create_payload = list(
    (
        dict(
            nonprocessed={"sex": "male"},
            processed={"sex": 0},
        ),
        dict(
            nonprocessed={"sex": "female"},
            processed={"sex": 1},
        ),
    )
)

dataset_rows_create_wrong_dataset_payload = list(
    (
        dict(
            dataset_id = "1234567890",
            nonprocessed={"sex": "male"},
            processed={"sex": 0},
        ),
        dict(
            dataset_id = "1234567890",
            nonprocessed={"sex": "female"},
            processed={"sex": 1},
        ),
    )
)

inference_row_create_payload = dict(
    timestamp=str(datetime.now()),
    nonprocessed={"sex": "female"},
    processed={"sex": 1},
    actual={"actual": 1},
)

inference_row_create_many_payload = list(
    (
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"sex": "male"},
            processed={"sex": 0},
            actual={"actual": 2},
        ),
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"sex": "non-binary"},
            processed={"sex": 2},
            actuals={"actual": 3},
        ),
    )
)
