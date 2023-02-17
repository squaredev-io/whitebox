import streamlit as st
import numpy as np
from utils.export import structure
from utils.transformation import (
    get_dataframe_from_classification_performance_dict,
    get_dataframe_from_regression_performance_dict,
)
from utils.graphs import create_line_graph


def create_performance_graphs(performance_df, perf_column):
    viz_df = performance_df[[perf_column, "timestamp"]]
    viz_df.columns = ["score (%)", "time"]
    mean_score = round(np.mean(viz_df["score (%)"]), 4) * 100
    subtitle = str(mean_score) + " %"
    create_line_graph(viz_df, "time", "score (%)", perf_column, subtitle, 400, 380)


def create_performance_tab(performance_dict, model):
    with st.spinner("Loading performance of the model..."):
        structure()
        st.title("Performance")
        # Set the graphs in two columns (side by side)
        col1, col2 = st.columns(2)

        if (model["type"] == "binary") | (model["type"] == "multi_class"):
            performance_df = get_dataframe_from_classification_performance_dict(
                performance_dict
            )
        else:
            # For now the only case is regression
            performance_df = get_dataframe_from_regression_performance_dict(
                performance_dict
            )
        # Need to keep only the metrics columns to be visualised as separeted graphs
        perf_columns = performance_df.drop("timestamp", axis=1).columns

        for i in range(len(perf_columns)):
            if (i % 2) == 0:
                with col1:
                    create_performance_graphs(performance_df, perf_columns[i])
            else:
                with col2:
                    create_performance_graphs(performance_df, perf_columns[i])
