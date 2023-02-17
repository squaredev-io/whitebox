import streamlit as st
import pandas as pd
from utils.export import structure
from utils.transformation import (
    get_recent_alert,
    combine_monitor_with_alert_for_monitors,
)


def add_new_monitor():

    new_monitor_name = st.text_input("Monitor name")
    if new_monitor_name:
        monitor_option = st.selectbox(
            "Select use case", ("Drift", "Data Quality", "Model performance")
        )
        monitor_option_check = st.checkbox("Select static threshold")

        if monitor_option_check:
            lower_threshold = st.number_input(
                "Lower threshold", min_value=0.0, max_value=1.0, key="lower"
            )
            upper_threshold = st.number_input(
                "Upper threshold", min_value=0.0, max_value=1.0, key="upper"
            )
            threshold_option_check = st.checkbox("Set actions")

            if threshold_option_check:
                st.write("Alert severity")
                severity = st.radio(
                    "What alert severity should be associated with the notifications being sent?",
                    ["Low", "Medium", "High"],
                )
                st.write("Notifications")
                new_monitor_name = st.text_input(
                    "Notifications will be sent via email. Please provide your email below:"
                )

                setup_button = st.button("Complete setup")
                if setup_button:
                    # Run the pipeline for the connection with the db here
                    st.write("The new monitor has be created!")
                    st.write(
                        "Please uncheck the 'Add new monitor' checkbox at the top to go back."
                    )


def basic_monitor_page(show_df, merged_df):
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


def create_monitors_tab(monitors, alerts):
    """ """
    with st.spinner("Loading monitors..."):
        structure()
        st.title("Monitors")

        monitors_df = pd.DataFrame(monitors)
        alerts_df = pd.DataFrame(alerts)

        # We need to find the recent alerts for each monitor
        # then we need them to get their decriptions to show into the
        # monitors tab
        recent_alerts_df = get_recent_alert(alerts_df)
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
        basic_monitor_page(show_df, merged_df)
