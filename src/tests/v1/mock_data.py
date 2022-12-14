from datetime import datetime
from src.schemas.model import ModelType
from sklearn.datasets import load_breast_cancer, load_wine
import pandas as pd
import random

from src.schemas.modelMonitor import AlertSeverity, MonitorMetrics, MonitorStatus

user_create_payload = dict(username="admin")

model_binary_create_payload = dict(
    name="Model 1",
    description="Model 1 description",
    type=ModelType.binary,
    features={
        "feature1": "numerical",
        "feature2": "numerical",
        "feature3": "numerical",
        "feature4": "numerical",
        "target": "numerical",
    },
    labels={"label_1": 0, "label_2": 1},
    prediction="target",
    probability="n/a",
)

model_multi_create_payload = dict(
    name="Model 1",
    description="Model 1 description",
    type=ModelType.multi_class,
    features={
        "feature1": "numerical",
        "feature2": "numerical",
        "feature3": "numerical",
        "feature4": "numerical",
        "target": "numerical",
    },
    labels={"label_1": 0, "label_2": 1, "label_3": 2},
    prediction="target",
    probability="n/a",
)

model_update_payload = dict(
    name="Model 1 - categorical",
    description="Model 1 description",
)

# dataset rows data for both binary and multiclass models
df_load_multi = load_wine()
df_multi = pd.DataFrame(df_load_multi.data, columns=df_load_multi.feature_names)
df_multi["target"] = df_load_multi.target
df_multi = df_multi.tail(100)

dict_multi_data = df_multi.to_dict(orient="records")
dataset_rows_create_multi_class_payload = [
    {"processed": x, "nonprocessed": x} for x in dict_multi_data
]

df_load_binary = load_breast_cancer()
df_binary = pd.DataFrame(df_load_binary.data, columns=df_load_binary.feature_names)
df_binary["target"] = df_load_binary.target
df_binary = df_binary.tail(100)

dict_binary_data = df_binary.to_dict(orient="records")
dataset_rows_create_binary_payload = [
    {"processed": x, "nonprocessed": x} for x in dict_binary_data
]

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


# inference rows data for both binary and multiclaas models
df_multi_inference = df_multi.tail(10)

dict_inferences = df_multi_inference.to_dict(orient="records")
inference_row_create_many_multi_payload = [
    {
        "timestamp": str(datetime.now()),
        "processed": x,
        "nonprocessed": x,
        "actual": random.randint(0, 1),
    }
    for x in dict_inferences
]

inference_row_create_single_row_payload = inference_row_create_many_multi_payload[0]

# This is the body of the request coming from the sdk
df_binary_inference = df_binary.tail(10)

dict_inferences = df_binary_inference.to_dict(orient="records")
inference_row_create_many_binary_payload = [
    {
        "timestamp": str(datetime.now()),
        "processed": x,
        "nonprocessed": x,
        "actual": random.randint(0, 1),
    }
    for x in dict_inferences
]

model_monitor_accuracy_create_payload = dict(
    name="accuracy monitor ",
    status=MonitorStatus.active,
    metric=MonitorMetrics.accuracy,
    lower_threshold=0.85,
    severity=AlertSeverity.low,
    email="example@whitebox.io",
)

model_monitor_f1_create_payload = dict(
    name="f1 Monitor",
    status=MonitorStatus.active,
    metric=MonitorMetrics.f1,
    lower_threshold=0.85,
    severity=AlertSeverity.low,
    email="example@whitebox.io",
)

model_monitor_data_drift_create_payload = dict(
    name="data drift monitor",
    status=MonitorStatus.active,
    metric=MonitorMetrics.data_drift,
    feature="concavity error",
    severity=AlertSeverity.low,
    email="example@whitebox.io",
)
