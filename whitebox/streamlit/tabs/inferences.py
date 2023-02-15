import streamlit as st
from utils.transformation import convert_inference_dict_to_df
from utils.export import structure


def highlight_rows(row, pred_column):
    actual = row.loc["actual"]
    pred = row.loc[pred_column]
    if actual != pred:
        color = "#8FC4C7"
    else:
        color = ""

    return ["background-color: {}".format(color) for r in row]


def create_inferences_tab(inf, pred_column):
    """ """
    with st.spinner("Loading inferences..."):
        structure()
        st.title("Inferences")

        inf_df = convert_inference_dict_to_df(inf, pred_column)
        # Style and mark the columns when actual is not equal to prediction
        inf_df = inf_df.style.apply(lambda x: highlight_rows(x, pred_column), axis=1)
        st.dataframe(inf_df, width=1200, height=390)
