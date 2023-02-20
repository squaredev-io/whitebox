import streamlit as st
import pandas as pd
import numpy as np
from utils.export import structure
from utils.transformation import (
    get_dataframe_from_classification_performance_metrics,
    get_dataframe_from_regression_performance_metrics,
)
from utils.graphs import create_line_graph

from typing import Union, List
import os, sys

sys.path.insert(0, os.path.abspath("./"))
from whitebox.schemas.model import Model
from whitebox.schemas.performanceMetric import (
    RegressionMetrics,
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
)


def create_performance_graphs(performance_df: pd.DataFrame, perf_column: str) -> None:
    """
    Creates a graph based on a performance metric
    """
    viz_df = performance_df[[perf_column, "timestamp"]]
    viz_df.columns = ["score (%)", "time"]
    mean_score = round(np.mean(viz_df["score (%)"]) * 100, 2)
    subtitle = str(mean_score) + " %"
    create_line_graph(viz_df, "time", "score (%)", perf_column, subtitle, 400, 380)


def create_performance_tab(
    performance: Union[
        List[RegressionMetrics],
        List[BinaryClassificationMetrics],
        List[MultiClassificationMetrics],
    ],
    model: Model,
) -> None:
    """
    Creates the performance tab in Streamlit
    """

    with st.spinner("Loading performance of the model..."):
        structure()
        st.title("Performance")
        # Set the graphs in two columns (side by side)
        col1, col2 = st.columns(2)

        if (model["type"] == "binary") | (model["type"] == "multi_class"):
            performance_df = get_dataframe_from_classification_performance_metrics(
                performance
            )
        else:
            # For now the only case is regression
            performance_df = get_dataframe_from_regression_performance_metrics(
                performance
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
