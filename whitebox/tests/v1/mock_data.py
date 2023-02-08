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
    labels={"label_1": 0, "label_2": 1},
    prediction="target",
)

model_multi_create_payload = dict(
    name="Model 2",
    description="Model 2 description",
    type=ModelType.multi_class,
    labels={"label_1": 0, "label_2": 1, "label_3": 2},
    prediction="target",
)

model_multi_2_create_payload = dict(
    name="Model 3",
    description="Model 3 description",
    type=ModelType.multi_class,
    labels={"label_1": 0, "label_2": 1, "label_3": 2},
    prediction="target",
)

model_multi_3_create_payload = dict(
    name="Model 4",
    description="Model 4 description",
    type=ModelType.multi_class,
    labels={"label_1": 0, "label_2": 1, "label_3": 2},
    prediction="target",
)

model_regression_create_payload = dict(
    name="Regression Model",
    description="Regression Model description",
    type=ModelType.regression,
    prediction="target",
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

model_monitor_concept_drift_create_payload = dict(
    name="concept drift monitor",
    status=MonitorStatus.active,
    metric=MonitorMetrics.concept_drift,
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

performance_metrics_report_payload = [
    {
        "id": "f7030044-e0c2-4493-8aea-f66e6564efb7",
        "created_at": "2023-02-06T09:53:00.343616",
        "updated_at": "2023-02-06T09:53:00.343616",
        "model_id": "dbb7f384-cf46-4884-bca3-7787e049a3d5",
        "timestamp": "2023-02-06T09:53:00.343548",
        "accuracy": 0.6,
        "precision": 0.25,
        "recall": 0.5,
        "f1": 0.3333333333333333,
        "true_negative": 5,
        "false_positive": 3,
        "false_negative": 1,
        "true_positive": 1,
    }
]

descriptive_statistics_report_payload = [
    {
        "id": "d4f18837-65f6-45c2-af7c-34dcdc4aabf9",
        "created_at": "2023-02-06T09:53:00.370639",
        "updated_at": "2023-02-06T09:53:00.370639",
        "model_id": "bc01a212-b01e-48b4-aeb5-4a0a3cfa3c98",
        "timestamp": "2023-02-06T09:53:00.370617",
        "feature_metrics": {
            "missing_count": {
                "alcohol": 0,
                "malic_acid": 0,
                "ash": 0,
                "alcalinity_of_ash": 0,
                "magnesium": 0,
                "total_phenols": 0,
                "flavanoids": 0,
                "nonflavanoid_phenols": 0,
                "proanthocyanins": 0,
                "color_intensity": 0,
                "hue": 0,
                "od280/od315_of_diluted_wines": 0,
                "proline": 0,
                "target": 0,
            },
            "non_missing_count": {
                "alcohol": 10,
                "malic_acid": 10,
                "ash": 10,
                "alcalinity_of_ash": 10,
                "magnesium": 10,
                "total_phenols": 10,
                "flavanoids": 10,
                "nonflavanoid_phenols": 10,
                "proanthocyanins": 10,
                "color_intensity": 10,
                "hue": 10,
                "od280/od315_of_diluted_wines": 10,
                "proline": 10,
                "target": 10,
            },
            "mean": {
                "alcohol": 13.379000000000001,
                "malic_acid": 3.564,
                "ash": 2.493,
                "alcalinity_of_ash": 21.6,
                "magnesium": 102.3,
                "total_phenols": 1.6620000000000001,
                "flavanoids": 0.699,
                "nonflavanoid_phenols": 0.44499999999999995,
                "proanthocyanins": 1.1889999999999998,
                "color_intensity": 8.595999899999999,
                "hue": 0.6399999999999999,
                "od280/od315_of_diluted_wines": 1.6970000000000003,
                "proline": 674.5,
                "target": 2.0,
            },
            "minimum": {
                "alcohol": 12.2,
                "malic_acid": 2.39,
                "ash": 2.26,
                "alcalinity_of_ash": 19.0,
                "magnesium": 86.0,
                "total_phenols": 1.25,
                "flavanoids": 0.49,
                "nonflavanoid_phenols": 0.27,
                "proanthocyanins": 0.64,
                "color_intensity": 5.5,
                "hue": 0.57,
                "od280/od315_of_diluted_wines": 1.56,
                "proline": 470.0,
                "target": 2.0,
            },
            "maximum": {
                "alcohol": 14.16,
                "malic_acid": 5.65,
                "ash": 2.86,
                "alcalinity_of_ash": 25.0,
                "magnesium": 120.0,
                "total_phenols": 2.05,
                "flavanoids": 0.96,
                "nonflavanoid_phenols": 0.56,
                "proanthocyanins": 1.54,
                "color_intensity": 10.2,
                "hue": 0.74,
                "od280/od315_of_diluted_wines": 1.92,
                "proline": 840.0,
                "target": 2.0,
            },
            "sum": {
                "alcohol": 133.79000000000002,
                "malic_acid": 35.64,
                "ash": 24.93,
                "alcalinity_of_ash": 216.0,
                "magnesium": 1023.0,
                "total_phenols": 16.62,
                "flavanoids": 6.989999999999999,
                "nonflavanoid_phenols": 4.449999999999999,
                "proanthocyanins": 11.889999999999999,
                "color_intensity": 85.959999,
                "hue": 6.3999999999999995,
                "od280/od315_of_diluted_wines": 16.970000000000002,
                "proline": 6745.0,
                "target": 20.0,
            },
            "standard_deviation": {
                "alcohol": 0.5907894906159238,
                "malic_acid": 1.1073311258256142,
                "ash": 0.2058613341278272,
                "alcalinity_of_ash": 2.3664319132398464,
                "magnesium": 11.80442478244681,
                "total_phenols": 0.24334703157790474,
                "flavanoids": 0.14224001624796806,
                "nonflavanoid_phenols": 0.08396427811873335,
                "proanthocyanins": 0.3045743842734572,
                "color_intensity": 1.4311393049673125,
                "hue": 0.05291502622129182,
                "od280/od315_of_diluted_wines": 0.12356284950492914,
                "proline": 130.39363481397396,
                "target": 0.0,
            },
            "variance": {
                "alcohol": 0.34903222222222274,
                "malic_acid": 1.2261822222222223,
                "ash": 0.04237888888888891,
                "alcalinity_of_ash": 5.599999999999999,
                "magnesium": 139.34444444444443,
                "total_phenols": 0.059217777777777765,
                "flavanoids": 0.02023222222222222,
                "nonflavanoid_phenols": 0.0070500000000000024,
                "proanthocyanins": 0.09276555555555556,
                "color_intensity": 2.048159710222322,
                "hue": 0.002800000000000001,
                "od280/od315_of_diluted_wines": 0.015267777777777769,
                "proline": 17002.5,
                "target": 0.0,
            },
        },
    }
]

drifting_metrics_report_payload = [
    {
        "id": "d11f2313-12e3-4533-b16d-7689175ad617",
        "created_at": "2023-02-06T09:53:00.450466",
        "updated_at": "2023-02-06T09:53:00.450466",
        "model_id": "e8e5ff00-0212-4a1e-bcdb-0ef9183c867f",
        "timestamp": "2023-02-06T09:53:00.450435",
        "concept_drift_summary": {
            "concept_drift_summary": {
                "column_name": "target",
                "column_type": "cat",
                "stattest_name": "Z-test p_value",
                "drift_score": 0.0010364142456651404,
                "drift_detected": True,
                "stattest_threshold": 0.05,
            },
            "column_correlation": {
                "column_name": "target",
                "current": {},
                "reference": {},
            },
        },
        "data_drift_summary": {
            "number_of_columns": 13,
            "number_of_drifted_columns": 7,
            "share_of_drifted_columns": 0.5384615384615384,
            "dataset_drift": True,
            "drift_by_columns": {
                "alcalinity_of_ash": {
                    "column_name": "alcalinity_of_ash",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.5163177458201748,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
                "alcohol": {
                    "column_name": "alcohol",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.0012612112534500996,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "ash": {
                    "column_name": "ash",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.23438597334285016,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
                "color_intensity": {
                    "column_name": "color_intensity",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.00015242693342585546,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "flavanoids": {
                    "column_name": "flavanoids",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.0003384276858653337,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "hue": {
                    "column_name": "hue",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.0002500181491633883,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "magnesium": {
                    "column_name": "magnesium",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.08450859981880006,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
                "malic_acid": {
                    "column_name": "malic_acid",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.033698127881912385,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "nonflavanoid_phenols": {
                    "column_name": "nonflavanoid_phenols",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.30861039864383094,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
                "od280/od315_of_diluted_wines": {
                    "column_name": "od280/od315_of_diluted_wines",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.0006076739224878145,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "proanthocyanins": {
                    "column_name": "proanthocyanins",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.09673060972050829,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
                "proline": {
                    "column_name": "proline",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.0328848734766648,
                    "drift_detected": True,
                    "threshold": 0.05,
                },
                "total_phenols": {
                    "column_name": "total_phenols",
                    "column_type": "num",
                    "stattest_name": "K-S p_value",
                    "drift_score": 0.082145120769578,
                    "drift_detected": False,
                    "threshold": 0.05,
                },
            },
        },
    }
]

inference_row_xai_payload = {
    "mean perimeter": -0.23641989216827916,
    "mean concavity": -0.16854638344893477,
    "worst radius": -0.16657884627852115,
    "mean concave points": -0.1260514980862101,
    "worst perimeter": -0.08533726601274261,
    "worst texture": -0.07905090544100012,
    "mean texture": -0.05969642438812264,
    "worst concave points": -0.03310756238929911,
    "mean radius": -0.03244286722644983,
    "worst symmetry": 0.02852296352595751,
}
