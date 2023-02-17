import streamlit as st
from utils.load import load_config, load_image
from utils.export import display_links, center_image
from typing import List, Tuple, Union


def create_sidebar(model_names: List[str]) -> Tuple[Union[str, None, bool], bool]:
    """
    Creates the sidebar of a Streamlit app

    Args:
        model_names (List[str]): _description_

    Returns:
        Tuple[Union[str, None, bool], bool]: _description_
    """
    readme = load_config("config_readme.toml")
    center_image()
    st.sidebar.image(load_image("logo.png"), width=120)
    display_links(readme["links"]["repo"])

    st.sidebar.write(
        "Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes."
    )

    model_option = st.sidebar.selectbox(
        "Please select one of your models below and then check the 'Ok':",
        model_names,
        help=readme["tooltips"]["model_option"],
    )
    # button = st.sidebar.button("Ok")
    button = st.sidebar.checkbox("Ok")

    return model_option, button
