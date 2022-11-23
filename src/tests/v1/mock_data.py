from datetime import datetime
from src.schemas.model import ModelType

user_create_payload = dict(username="admin")
users_in_db = dict(amount=1)
user_update_payload = dict(username="admin1")

model_binary_create_payload = dict(
    name="Model 1",
    description="Model 1 description",
    type=ModelType.binary,
    features={"y_testing_binary": "categorical"},
    labels={"label_1": 1, "label_2": 2},
    prediction="y_prediction_binary",
    probability="n/a",
)

model_multi_create_payload = dict(
    name="Model 1",
    description="Model 1 description",
    type=ModelType.multi_class,
    features={"y_testing_multi": "categorical"},
    labels={"label_1": 1, "label_2": 2},
    prediction="y_prediction_multi",
    probability="n/a",
)

model_update_payload = dict(
    name="Model 1 - categorical",
    description="Model 1 description",
)

dataset_rows_create_multi_class_payload = list(
    (
        dict(
            nonprocessed={"y_testing_multi": 2, "y_prediction_multi": 2},
            processed={"y_testing_multi": 2, "y_prediction_multi": 2},
        ),
        dict(
            nonprocessed={"y_testing_multi": 1, "y_prediction_multi": 1},
            processed={"y_testing_multi": 1, "y_prediction_multi": 1},
        ),
    )
)


dataset_rows_create_binary_payload = list(
    (
        dict(
            nonprocessed={"y_testing_binary": 0, "y_prediction_binary": 0},
            processed={"y_testing_binary": 0, "y_prediction_binary": 0},
        ),
        dict(
            nonprocessed={"y_testing_binary": 1, "y_prediction_binary": 1},
            processed={"y_testing_binary": 1, "y_prediction_binary": 1},
        ),
    )
)

dataset_rows_create_wrong_model_payload = list(
    (
        dict(
            model_id="1234567890",
            nonprocessed={"sex": "male"},
            processed={"sex": 0},
        ),
        dict(
            model_id="1234567890",
            nonprocessed={"sex": "female"},
            processed={"sex": 1},
        ),
    )
)

inference_row_create_payload = dict(
    timestamp=str(datetime.now()),
    nonprocessed={"y_testing_multi": 2, "y_prediction_multi": 2},
    processed={"y_testing_multi": 2, "y_prediction_multi": 2},
    actual=2,
)

inference_row_create_many_multi_payload = list(
    (
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"y_testing_multi": 1, "y_prediction_multi": 1},
            processed={"y_testing_multi": 1, "y_prediction_multi": 1},
            actual=1,
        ),
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"y_testing_multi": 2, "y_prediction_multi": 1},
            processed={"y_testing_multi": 2, "y_prediction_multi": 1},
            actual=2,
        ),
    )
)

# This is the body of the request coming from the sdk
inference_row_create_many_binary_payload = list(
    (
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"y_testing_binary": 0, "y_prediction_binary": 1},
            processed={"y_testing_binary": 0, "y_prediction_binary": 1},
            actual=1,
        ),
        dict(
            timestamp=str(datetime.now()),
            nonprocessed={"y_testing_binary": 1, "y_prediction_binary": 1},
            processed={"y_testing_binary": 1, "y_prediction_binary": 1},
            actual=0,
        ),
    )
)
