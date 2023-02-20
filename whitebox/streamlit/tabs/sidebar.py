import streamlit as st
from utils.load import load_config, load_image
from utils.export import display_links, center_image
from typing import List, Tuple, Union
from whitebox import Whitebox
from utils.transformation import get_models_names


def create_sidebar() -> Tuple[
    Union[str, None, bool],
    Union[List[str], None],
    Union[bool, None],
    Union[Whitebox, None],
]:
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
    st.sidebar.write("Begin immediately by defining the below settings:")

    host_option = st.sidebar.text_input(
        "Paste here your host url:",
        max_chars=21,
        placeholder="http://127.0.0.1:8000",
        value="http://127.0.0.1:8000",
    )

    api_key_option = st.sidebar.text_input(
        "Paste here your api key:",
        max_chars=64,
        type="password",
        placeholder="your api key",
    )
    setting_confirmation = st.sidebar.checkbox(
        "I'm ok, proceed with the above settings"
    )

    if setting_confirmation:
        wb = Whitebox(
            host=host_option,
            api_key=api_key_option,
        )
        models_list = wb.get_models()
        model_names = get_models_names(models_list)

        model_option = st.sidebar.selectbox(
            "Please select one of the found models below and then check 'Ok':",
            model_names,
            help=readme["tooltips"]["model_option"],
        )
        checkbox = st.sidebar.checkbox("Ok")

        return model_option, models_list, checkbox, wb
    else:
        return None, None, False, None
