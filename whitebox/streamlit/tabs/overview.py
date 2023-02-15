import streamlit as st
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from cards import *
from utils.export import structure
from utils.load import load_config


def create_overview_tab(model, confusion_matrix, base_evaluation_metrics):
    with st.spinner("Loading overview of the model..."):
        readme = load_config("config_readme.toml")
        structure()
        st.title("Overview")
        st.write(card(model["name"], model["type"], model["description"]))
        st.header("Performance")

        with st.expander("See explanation"):
            st.write(readme["tooltips"]["overview_performance"])

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

        st.header("Confusion matrix")
        disp = ConfusionMatrixDisplay(
            confusion_matrix=confusion_matrix,
            display_labels=list(model["labels"].values()),
        )
        fig, ax = plt.subplots(figsize=(5, 5))
        disp.plot(ax=ax)
        st.pyplot()
