import streamlit as st
import pandas as pd
from utils.export import structure


def combine_monitor_with_alert_for_alerts(monitor_df, alert_df):

    merged_df = pd.merge(
        monitor_df[["id", "metric", "name"]],
        alert_df[["model_monitor_id", "timestamp", "description"]],
        how="right",
        left_on="id",
        right_on="model_monitor_id",
    )
    return merged_df


def create_alerts_tab(alerts, monitors):
    """ """

    total_alerts = len(alerts)
    with st.spinner("Loading alerts..."):
        structure()
        st.title("Alerts (" + str(total_alerts) + ")")

        alerts_df = pd.DataFrame(alerts)
        monitors_df = pd.DataFrame(monitors)

        merged_df = combine_monitor_with_alert_for_alerts(monitors_df, alerts_df)
        show_df = merged_df[["timestamp", "metric", "description", "name"]]
        show_df.columns = [
            "Anomaly timestamp",
            "Metric",
            "Anomaly details",
            "Monitor Name",
        ]
        print(show_df)
        st.dataframe(show_df, width=1200, height=300)
