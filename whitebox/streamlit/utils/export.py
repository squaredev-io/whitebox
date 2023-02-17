from typing import Any, Dict, List
import streamlit as st


def display_links(repo_link: str) -> None:
    """Displays a repository"""
    st.sidebar.markdown(
        f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
        unsafe_allow_html=True,
    )


def structure() -> None:
    """Structures the tabs in Streamlit"""
    st.markdown(
        """
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                """,
        unsafe_allow_html=True,
    )


def center_image() -> None:
    """Markdown for seting logo in the center"""
    st.markdown(
        """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def text_markdown(text: str, color: str, font_size: str) -> None:
    """Sets a text in specific color and font size"""
    st.markdown(
        f'<p style="color:{color};{font_size}:12px;border-radius:2%;">{text}</p>',
        unsafe_allow_html=True,
    )
