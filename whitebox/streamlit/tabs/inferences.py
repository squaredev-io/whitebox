import streamlit as st
import pandas as pd
from utils.transformation import convert_inference_to_df
from utils.export import structure
import time

import os, sys
sys.path.insert(0, os.path.abspath("./"))
from whitebox.schemas.inferenceRow import InferenceRow
from typing import List


def highlight_rows(row: pd.DataFrame, pred_column: str):
    """
    Part of styling function of dataframe.
    It highlights the rows where actual is inequal to to prediction
    """
    actual = row.loc["actual"]
    pred = row.loc[pred_column]
    if actual != pred:
        color = "#8FC4C7"
    else:
        color = ""

    return ["background-color: {}".format(color) for r in row]


def viz_inference_df(inf_df: pd.DataFrame, pred_column: str):
    """
    Visualises the highlighted dataframe in Streamlit
    """
    # Style and mark the columns when actual is not equal to prediction
    inf_df = inf_df.style.apply(lambda x: highlight_rows(x, pred_column), axis=1)
    st.dataframe(inf_df, width=1200, height=390)


def create_inferences_tab(inf: List[InferenceRow], pred_column: str) -> None:
    """
    Creates the Inferences tab in Streamlit.
    It visualises the dataframe of the inferences and also spawns
    the explanation part based on explainability.
    """
    with st.spinner("Loading inferences..."):
        structure()
        st.title("Inferences")
        inf_df = convert_inference_to_df(inf, pred_column)

    explain = st.checkbox("Explain inferences")
    if explain:
        col1, col2 = st.columns(2)

        with col1:
            # TODO: Add filter for dates (eg. Show data from 'last month')
            viz_inference_df(inf_df, pred_column)

        with col2:
            text_input = st.text_input(
                "Explain an inference based on id:", placeholder="an inference id"
            )

            if text_input:
                with st.spinner("Loading explanations for id: " + text_input):
                    time.sleep(8)

    else:
        viz_inference_df(inf_df, pred_column)
