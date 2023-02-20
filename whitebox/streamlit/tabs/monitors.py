import streamlit as st
import pandas as pd
from utils.export import structure
from utils.transformation import (
    get_recent_alert,
    combine_monitor_with_alert_for_monitors,
)
from utils.load import load_config
from utils.export import text_markdown

from typing import List
import os, sys

sys.path.insert(0, os.path.abspath("./"))
from whitebox.schemas.alert import Alert
from whitebox.schemas.modelMonitor import ModelMonitor


def add_new_monitor() -> None:
    """
    Spawns the section of the addition of a new monitor
    """
    readme = load_config("config_readme.toml")
    new_monitor_name = st.text_input(
        "Monitor name",
        max_chars=30,
        help=readme["tooltips"]["monitor_name"],
        placeholder="Model name",
    )
    if new_monitor_name:
        monitor_option = st.selectbox(
            "Select use case",
            ("Drift", "Data Quality", "Model performance"),
            help=readme["tooltips"]["monitor_use_case"],
        )
        monitor_option_check = st.checkbox("Select static threshold")

        if monitor_option_check:

            st.write(
                text_markdown(
                    readme["tooltips"]["alert_trig_monitor"], "#525462", "12px"
                )
            )
            lower_threshold = st.number_input(
                "Lower threshold",
                min_value=0.0,
                max_value=1.0,
                key="lower",
                help=readme["tooltips"]["stat_thresh_monitor"],
            )
            upper_threshold = st.number_input(
                "Upper threshold",
                min_value=0.0,
                max_value=1.0,
                key="upper",
                help=readme["tooltips"]["stat_thresh_monitor"],
            )
            threshold_option_check = st.checkbox("Set actions")

            if threshold_option_check:
                st.write("Alert severity")
                st.write(
                    text_markdown(
                        readme["tooltips"]["alert_severity_monitor"], "#525462", "12px"
                    )
                )
                severity = st.radio(
                    "Alert severity",
                    ["Low", "Medium", "High"],
                    label_visibility="collapsed",
                )

                st.write("Notifications")
                st.write(
                    text_markdown(
                        readme["tooltips"]["notifications_monitor"], "#525462", "12px"
                    )
                )
                new_monitor_name = st.text_input(
                    "Notifications",
                    placeholder="Your email...",
                    label_visibility="collapsed",
                )

                setup_button = st.button("Complete setup")
                if setup_button:
                    # Run the pipeline for the connection with the db here
                    st.write("The new monitor has be created!")
                    st.write(
                        "Please uncheck the 'Add new monitor' checkbox at the top to go back."
                    )


def basic_monitor_page(show_df: pd.DataFrame, merged_df: pd.DataFrame) -> None:
    """
    Create the basic monitor page part.
    Displays the dataframe of the monitors and adds filters
    for activity and inactivity of found monitors.
    """

    st.dataframe(show_df, width=1200, height=300)
    multiselect = st.multiselect(
        "Search and filter for monitors", merged_df["name"].values.tolist()
    )
    if multiselect:
        filtered_df = show_df[show_df["Name"].isin(multiselect)]
        st.dataframe(filtered_df, width=1200, height=200)

        status = st.checkbox("Change the status of the selected monitors")
        if status:
            status_slider = st.select_slider(
                "Select the status of the selected monitor",
                ["Active", "", "Inactive"],
                value=(""),
            )

            if status_slider == "Active":
                # here we need the connection with db
                st.write(
                    "The status of the selected monitors has been updated to 'Active'!"
                )
            elif status_slider == "Inactive":
                # here we need the connection with db
                st.write(
                    "The status of the selected monitors has been updated to 'Inactive'!"
                )


def create_monitors_tab(monitors: List[ModelMonitor], alerts: List[Alert]):
    """
    Creates the monitors tabs in Streamlit
    """
    with st.spinner("Loading monitors..."):
        structure()
        st.title("Monitors")

        monitors_df = pd.DataFrame(monitors)
        alerts_df = pd.DataFrame(alerts)

        # We need to find the recent alerts for each monitor
        # then we need them to get their decriptions to show into the
        # monitors tab
        recent_alerts_df = get_recent_alert(alerts_df)
        if len(monitors_df) > 0:
            merged_df = combine_monitor_with_alert_for_monitors(
                monitors_df, recent_alerts_df
            )

            show_df = merged_df[["status", "name", "updated_at", "description"]]
            show_df.columns = ["Status", "Name", "Last update", "Anomaly activity"]

    add_new_monitor_check = st.checkbox(
        "Add new monitor",
        key="test",
    )
    if add_new_monitor_check:
        add_new_monitor()
    else:
        if len(monitors_df) > 0:
            basic_monitor_page(show_df, merged_df)
