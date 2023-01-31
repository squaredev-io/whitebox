from datetime import datetime
from whitebox.schemas.model import ModelType
from sklearn.datasets import load_breast_cancer, load_wine, load_diabetes
import pandas as pd
import random
from copy import deepcopy

from whitebox.schemas.modelMonitor import AlertSeverity, MonitorMetrics, MonitorStatus

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
    name="Model 2",
    description="Model 2 description",
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

model_multi_2_create_payload = dict(
    name="Model 3",
    description="Model 3 description",
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

model_multi_3_create_payload = dict(
    name="Model 4",
    description="Model 4 description",
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

model_regression_create_payload = dict(
    name="Regression Model",
    description="Regression Model description",
    type=ModelType.regression,
    features={
        "feature1": "numerical",
        "feature2": "numerical",
        "feature3": "numerical",
        "feature4": "numerical",
        "target": "numerical",
    },
    prediction="target",
    probability="n/a",
)

model_update_payload = dict(
    name="Model 1 - categorical",
    description="Model 1 description",
)

# dataset rows data for both binary and multiclass models
dataset_rows_single_row_column_payload = [
    {
        "nonprocessed": {},
        "processed": {"additionalProp1": 0, "additionalProp2": 0, "target": 1},
    }
]

dataset_rows_no_prediction_column_payload = [
    {
        "nonprocessed": {},
        "processed": {"additionalProp1": 0, "additionalProp2": 0},
    },
    {
        "nonprocessed": {},
        "processed": {"additionalProp1": 1, "additionalProp2": 0},
    },
]

dataset_rows_one_prediction_value_payload = [
    {
        "nonprocessed": {},
        "processed": {"additionalProp1": 0, "additionalProp2": 0, "target": 0},
    },
    {
        "nonprocessed": {},
        "processed": {"additionalProp1": 1, "additionalProp2": 0, "target": 0},
    },
]


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

df_load_reg = load_diabetes()
df_reg = pd.DataFrame(df_load_reg.data, columns=df_load_reg.feature_names)
df_reg["target"] = df_load_reg.target
df_reg = df_reg.tail(100)

dict_reg_data = df_reg.to_dict(orient="records")
dataset_rows_create_reg_payload = [
    {"processed": x, "nonprocessed": x} for x in dict_reg_data
]

dataset_rows_create_wrong_model_payload = list(
    (
        dict(
            model_id="wrong_model_id",
            nonprocessed={"sex": "male"},
            processed={"sex": 0},
        ),
        dict(
            model_id="wrong_model_id",
            nonprocessed={"sex": "female"},
            processed={"sex": 1},
        ),
    )
)


# inference rows data for both binary and multiclaas models
df_multi_inference = df_multi.tail(10)
dict_multi_inferences = df_multi_inference.to_dict(orient="records")
inference_row_create_many_multi_payload = [
    {
        "timestamp": str(datetime.now()),
        "processed": x,
        "nonprocessed": x,
        "actual": random.randint(0, 1),
    }
    for x in dict_multi_inferences
]

inference_row_create_single_row_payload = inference_row_create_many_multi_payload[0]
inference_row_create_many_multi_no_actual_payload = deepcopy(
    inference_row_create_many_multi_payload
)
for x in inference_row_create_many_multi_no_actual_payload:
    del x["actual"]

inference_row_create_many_multi_mixed_actuals_payload = (
    inference_row_create_many_multi_no_actual_payload
    + inference_row_create_many_multi_payload
)

# This is the body of the request coming from the sdk
df_binary_inference = df_binary.tail(10)
dict_binary_inferences = df_binary_inference.to_dict(orient="records")
inference_row_create_many_binary_payload = [
    {
        "timestamp": str(datetime.now()),
        "processed": x,
        "nonprocessed": x,
        "actual": random.randint(0, 1),
    }
    for x in dict_binary_inferences
]

df_reg_inference = df_reg.tail(10)
dict_reg_inferences = df_reg_inference.to_dict(orient="records")
inference_row_create_many_reg_payload = [
    {
        "timestamp": str(datetime.now()),
        "processed": x,
        "nonprocessed": x,
        "actual": random.randint(0, 1),
    }
    for x in dict_reg_inferences
]

timestamps = pd.Series(["2022-12-22T12:13:27.879738"] * 10)
mixed_actuals = pd.Series([0, 1, None, 1, 0, None, None, 1, 0, None])

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

model_monitor_precision_create_payload = dict(
    name="precision monitor",
    status=MonitorStatus.active,
    metric=MonitorMetrics.precision,
    lower_threshold=0.85,
    severity=AlertSeverity.low,
    email="example@whitebox.io",
)

model_monitor_r_square_create_payload = dict(
    name="r_square monitor",
    status=MonitorStatus.active,
    metric=MonitorMetrics.r_square,
    lower_threshold=0.85,
    severity=AlertSeverity.low,
    email="example@whitebox.io",
)
