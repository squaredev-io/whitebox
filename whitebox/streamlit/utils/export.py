from typing import Any, Dict, List
import streamlit as st


def display_links(repo_link: str) -> None:
    """Displays a repository"""
    st.sidebar.markdown(
        f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
        unsafe_allow_html=True,
    )


def structure():
    st.markdown(
        """
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                """,
        unsafe_allow_html=True,
    )
