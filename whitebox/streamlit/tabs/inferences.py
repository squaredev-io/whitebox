import streamlit as st
from utils.transformation import convert_inference_dict_to_df
from utils.export import structure


def create_inferences_tab(inf, pred_column):
    """ """
    with st.spinner("Loading model drift..."):
        structure()
        st.title("Inferences")

        inf_df = convert_inference_dict_to_df(inf, pred_column)
        st.dataframe(inf_df, width=1200, height=390)
