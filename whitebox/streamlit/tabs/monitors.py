import streamlit as st
import pandas as pd
from utils.export import structure


def get_recent_alert(alerts_df):
    """
    Function that gets alerts dataframe and results on the
    most recent alert row for each unique id
    """
    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"])
    # sort the dataframe by 'date' column in descending order
    alerts_df = alerts_df.sort_values(by="timestamp", ascending=False)
    # drop duplicates based on 'id' column, keeping only the first occurrence (most recent date)
    alerts_df = alerts_df.drop_duplicates(subset="model_monitor_id", keep="first")

    return alerts_df.reset_index(drop=True)


def combine_monitor_with_alert(monitor_df, alert_df):
    merged_df = pd.merge(
        monitor_df,
        alert_df[["model_monitor_id", "timestamp", "description"]],
        left_on="id",
        right_on="model_monitor_id",
    )
    return merged_df


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


def create_monitors_tab(monitors, alerts):
    """ """
    with st.spinner("Loading monitors..."):
        structure()
        st.title("Monitors")

        monitors_df = pd.DataFrame(monitors)
        alerts_df = pd.DataFrame(alerts)
        recent_alerts_df = get_recent_alert(alerts_df)
        merged_df = combine_monitor_with_alert(monitors_df, recent_alerts_df)
        show_df = merged_df[["status", "name", "timestamp", "description"]]

        add_new_monitor_check = st.checkbox(
            "Add new monitor",
            key="test",
        )
        if add_new_monitor_check:
            add_new_monitor()
        else:
            basic_monitor_page(show_df, merged_df)


def basic_monitor_page(show_df, merged_df):
    st.dataframe(show_df, width=1200, height=300)
    multiselect = st.multiselect(
        "Search and filter for monitors", merged_df["name"].values.tolist()
    )
    if multiselect:
        filtered_df = show_df[show_df["name"].isin(multiselect)]
        st.dataframe(filtered_df, width=1200, height=200)

        status = st.checkbox(
            "Do you want to change the status of the selected monitors?"
        )
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
