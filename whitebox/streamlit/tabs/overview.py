import streamlit as st
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from cards import *


def create_overview_tab(model, confusion_matrix, base_evaluation_metrics):
    st.markdown(
        """
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                """,
        unsafe_allow_html=True,
    )

    st.title("Overview")
    st.write(card(model["name"], model["type"], model["description"]))
    st.header("Performance")

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
        confusion_matrix=confusion_matrix, display_labels=list(model["labels"].values())
    )
    fig, ax = plt.subplots(figsize=(5, 5))
    disp.plot(ax=ax)
    st.pyplot()
