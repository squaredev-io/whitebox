import numpy as np
import pandas as pd
import streamlit as st
from typing import Dict, Union

from tabs.drifting import *
from tabs.sidebar import *
from tabs.overview import *
from tabs.performance import *
from tabs.inferences import *
from tabs.monitors import *
from tabs.alerts import *
from cards import *
from utils.transformation import get_model_from_name

from whitebox import Whitebox

# wb = Whitebox(
#     host="http://127.0.0.1:8000",
#     api_key="c37b902f5af13c43af33652770d7c51008f5e18b0cf4cf9cc870ab93bea98f3f",
# )
st.set_option("deprecation.showPyplotGlobalUse", False)

# ----------------------------------------------
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

# -----------------------------------
overview, performance, drifting, inferences, monitors, alerts = st.tabs(
    ["Overview", "Performance", "Drifting", "Inferences", "Monitors", "Alerts"]
)
model_option, models_list, checkbox, wb = create_sidebar()

if checkbox:
    model = get_model_from_name(models_list, model_option)
    pred_column = model["prediction"]
    model_id = model["id"]
    model_type = model["type"]
    # TODO: Need to connect this one with the db.
    with overview:
        create_overview_tab(model, cm, base_evaluation_metrics_binary_df)

    with performance:
        create_performance_tab(wb, model_id, model_type)

    with drifting:
        create_drift_tab(wb, model_id)

    with inferences:
        create_inferences_tab(wb, model_id, pred_column)

    with monitors:
        create_monitors_tab(wb, model_id, model_type)

    with alerts:
        create_alerts_tab(wb, model_id)
