import numpy as np
import pandas as pd
import streamlit as st
from typing import Dict, Union, List
from matplotlib import pyplot as plt
import json


from tabs.drifting import *
from tabs.sidebar import *
from tabs.overview import *
from tabs.performance import *
from tabs.inferences import *
from tabs.monitors import *
from tabs.alerts import *
from cards import *

st.set_option("deprecation.showPyplotGlobalUse", False)

# The below lines are temp until we have the performance metricc functionality
# ----------------------------------------
def format_evaluation_metrics_binary(
    accuracy: float,
    precision: float,
    recall: float,
    f1: float,
    tn: int,
    fp: int,
    fn: int,
    tp: int,
) -> Dict[str, Union[int, float]]:
    formated_metrics_for_binary = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "true_positive": tp,
    }

    return formated_metrics_for_binary


model_names = ["model test", "decision_tree", "random_forest", "custom_tf_model"]

model = {
    "id": "001",
    "name": "model test",
    "description": "a model for testing visualisations",
    "type": "binary",
    "target_column": "target",
    "labels": {"default": 0, "no_default": 1},
    "created_at": "2022-05-05",
    "updated_at": "2022-05-05",
}
evaluation_metrics_binary = format_evaluation_metrics_binary(
    0.64, 0.5, 0.11, 0.72, 1200, 600, 840, 260
)
evaluation_metrics_binary_df = pd.DataFrame(evaluation_metrics_binary, index=[0])
base_evaluation_metrics_binary_df = evaluation_metrics_binary_df[
    ["accuracy", "precision", "recall", "f1"]
]
# Conf matrix
first_part = [
    evaluation_metrics_binary["true_positive"],
    evaluation_metrics_binary["false_positive"],
]
second_part = [
    evaluation_metrics_binary["false_negative"],
    evaluation_metrics_binary["true_negative"],
]
cm = np.array([first_part, second_part])

f = open("whitebox/streamlit/mock/drift.json")
drift = json.load(f)
f.close()

f = open("whitebox/streamlit/mock/performance.json")
perf = json.load(f)
f.close()

f = open("whitebox/streamlit/mock/inferences.json")
inf = json.load(f)
f.close()

f = open("whitebox/streamlit/mock/monitors.json")
mon = json.load(f)
f.close()

f = open("whitebox/streamlit/mock/alerts.json")
al = json.load(f)
f.close()

pred_column = model["prediction"]

# -----------------------------------
overview, performance, drifting, inferences, monitors, alerts = st.tabs(
    ["Overview", "Performance", "Drifting", "Inferences", "Monitors", "Alerts"]
)

model_option, button = create_sidebar(model_names)

if button:
    with overview:
        create_overview_tab(model, cm, base_evaluation_metrics_binary_df)

    with performance:
        create_performance_tab(perf, model)

    with drifting:
        create_drift_tab(drift)

    with inferences:
        create_inferences_tab(inf, pred_column)

    with monitors:
        create_monitors_tab(mon, al)

    with alerts:
        create_alerts_tab(al, mon)
