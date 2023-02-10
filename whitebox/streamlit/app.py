import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
import streamlit as st
from typing import Dict, Union, List
from matplotlib import pyplot as plt
import json
import plotly.express as px

from utils.transformation import export_drift_timeseries_from_dict

from utils.load import load_config, load_image
from utils.export import display_links
from cards import *

st.set_option("deprecation.showPyplotGlobalUse", False)

# Load config
st.set_page_config(page_title="Whitebox", layout="wide")
readme = load_config("config_readme.toml")


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

f = open("streamlit/mock/drift.json")
drift = json.load(f)
f.close()

overview, performance, drifting, inferences, monitors, alerts = st.tabs(
    ["Overview", "Performance", "Drifting", "Inferences", "Monitors", "Alerts"]
)

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.image(load_image("logo.png"), width=120)


display_links(readme["links"]["repo"])
st.sidebar.write(
    "Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes."
)
model_option = st.sidebar.selectbox(
    "Please select one of your models below and then press 'Ok':",
    model_names,
    help=readme["tooltips"]["model_option"],
)
button = st.sidebar.button("Ok")

if button:
    with overview:
        st.markdown(
            """
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                """,
            unsafe_allow_html=True,
        )
        st.header("Model: " + model["name"])
        st.write(card(model["description"]))
        st.header("Performance")
        st.table(base_evaluation_metrics_binary_df)

        st.header("Confusion matrix")
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=list(model["labels"].values())
        )
        fig, ax = plt.subplots(figsize=(5, 5))
        disp.plot(ax=ax)
        st.pyplot()

    with drifting:
        value_df, drift_df = export_drift_timeseries_from_dict(drift)
        df_columns = value_df.drop("index", axis=1).columns
        common_tab, sep_tab = st.tabs(
            ["Common representation", "Separeted representation"]
        )
        with sep_tab:
            for column in df_columns:
                drift_detected = (drift_df[[column]] == True).any()[0]
                viz_df = value_df[[column, "index"]]
                viz_df.columns = ["drift_score", "time"]
                subtitle = ""
                if drift_detected:
                    subtitle = "Drift detected"
                fig = px.line(
                    viz_df,
                    x="time",
                    y="drift_score",
                    title=f"{column} <br><sup>{subtitle}</sup>",
                )
                st.plotly_chart(fig)
        with common_tab:
            drift_detected = True in drift_df.values
            subtitle = ""
            if drift_detected:
                subtitle = "Drift detected"
            fig = px.line(
                value_df,
                x="index",
                y=df_columns,
                title=f"All variables <br><sup>{subtitle}</sup>",
                markers=True,
            )
            st.plotly_chart(fig)
