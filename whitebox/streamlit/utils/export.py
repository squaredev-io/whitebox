from typing import Any, Dict, List
import streamlit as st


def display_links(repo_link: str) -> None:
    """Displays a repository"""
    st.sidebar.markdown(
        f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
        unsafe_allow_html=True,
    )
