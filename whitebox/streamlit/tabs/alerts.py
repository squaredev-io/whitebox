import streamlit as st
import pandas as pd
from utils.export import structure
from utils.transformation import combine_monitor_with_alert_for_alerts

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

import os, sys

sys.path.insert(0, os.path.abspath("./"))
from whitebox import Whitebox


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates filtering on top of a dataframe

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filter_checkbox = st.checkbox("Add filters")

    if not filter_checkbox:
        return df

    df = df.copy()

    # Convert datetimes into a standard format (datetime with no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    filter_container = st.container()

    with filter_container:
        filtering_columns = st.multiselect("Filter dataframe on", df.columns)

        for column in filtering_columns:
            left, right = st.columns((1, 20))

            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]

            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )

                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )

                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def create_alerts_tab(wb: Whitebox, model_id: str) -> None:
    """
    Creates the alerts tab in Streamlit.
    A table with all the alerts is visualised.
    """

    with st.spinner("Loading alerts..."):
        structure()
        monitors = wb.get_monitors(model_id)
        alerts = wb.get_alerts(model_id)
        total_alerts = len(alerts)
        st.title("Alerts (" + str(total_alerts) + ")")

        alerts_df = pd.DataFrame(alerts)
        monitors_df = pd.DataFrame(monitors)

        if (len(alerts_df) > 0) & (len(monitors_df) > 0):
            merged_df = combine_monitor_with_alert_for_alerts(monitors_df, alerts_df)
            show_df = merged_df[["timestamp", "metric", "description", "name"]]
            show_df.columns = [
                "Anomaly timestamp",
                "Metric",
                "Anomaly details",
                "Monitor Name",
            ]
            filtered_df = filter_dataframe(show_df)
            st.dataframe(filtered_df, width=1200, height=300)
