import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
from numpy import ndarray
from sklearn.metrics import ConfusionMatrixDisplay
from cards import *
from utils.export import structure
from utils.load import load_config

import os, sys

sys.path.insert(0, os.path.abspath("./"))
from whitebox.schemas.model import Model

# TODO: Need to connect this one with the db.
# Currently one shot running for training data is not supported!
def create_classification_performance_metrics(
    base_evaluation_metrics: pd.DataFrame,
) -> None:

    """
    Create performance metrics visualisation for classification model in Streamlit
    """
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        label="Accuracy",
        value=base_evaluation_metrics["accuracy"].iloc[0],
    )

    col2.metric(
        label="Precision",
        value=base_evaluation_metrics["precision"].iloc[0],
    )

    col3.metric(
        label="Recall",
        value=base_evaluation_metrics["recall"].iloc[0],
    )

    col4.metric(
        label="F1",
        value=base_evaluation_metrics["f1"].iloc[0],
    )


def create_regression_performance_metrics(
    base_evaluation_metrics: pd.DataFrame,
) -> None:
    """
    Create performance metrics visualisation for regression model in Streamlit
    """
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="R2",
        value=base_evaluation_metrics["r_square"].iloc[0],
    )

    col2.metric(
        label="MSE",
        value=base_evaluation_metrics["mean_squared_error"].iloc[0],
    )

    col3.metric(
        label="MAE",
        value=base_evaluation_metrics["mean_absolute_error"].iloc[0],
    )


def plot_confusion_matrix(confusion_matrix: ndarray, model: Model):
    st.header("Confusion matrix")
    disp = ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix,
        display_labels=list(model["labels"].values()),
    )
    fig, ax = plt.subplots(figsize=(5, 5))
    disp.plot(ax=ax)
    st.pyplot()


def create_overview_tab(
    model: Model, confusion_matrix: ndarray, base_evaluation_metrics: pd.DataFrame
) -> None:
    """
    Creates the overview tab in Streamlit
    """
    with st.spinner("Loading overview of the model..."):
        readme = load_config("config_readme.toml")
        structure()
        st.title("Overview")
        st.write(card(model["name"], model["type"], model["description"]))
        st.header("Performance")

        with st.expander("See explanation"):
            st.write(readme["tooltips"]["overview_performance"])

        if model["type"] == "binary":
            create_classification_performance_metrics(base_evaluation_metrics)
            plot_confusion_matrix(confusion_matrix, model)

        elif model["type"] == "multi_class":
            create_classification_performance_metrics(base_evaluation_metrics)

        elif model["type"] == "regression":
            create_regression_performance_metrics(base_evaluation_metrics)
