import streamlit as st
from utils.export import structure


def create_monitors_tab():
    """ """
    with st.spinner("Loading monitors..."):
        structure()
        st.title("Monitors")
