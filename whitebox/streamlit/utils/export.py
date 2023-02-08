from typing import Any, Dict, List
import streamlit as st


def display_links(repo_link: str) -> None:
    """Displays a repository and app links.

    Parameters
    ----------
    repo_link : str
        Link of git repository.
    article_link : str
        Link of medium article.
    """
    col1, col2 = st.sidebar.columns(2)
    col1.markdown(
        f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
        unsafe_allow_html=True,
    )
