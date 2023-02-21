import streamlit as st
from typing import Tuple, Dict, Any
import toml
from pathlib import Path
from PIL import Image


@st.cache_data(ttl=300)
def load_config(config_readme_filename: str) -> Dict[str, Any]:
    """Loads configuration files.

    Parameters
    ----------
    config_readme_filename : str
        Filename of readme configuration file.

    Returns
    -------
    dict
        Lib configuration file.
    dict
        Readme configuration file.
    """
    config_readme = toml.load(
        Path(f"whitebox/streamlit/config/{config_readme_filename}")
    )
    return dict(config_readme)


@st.cache_data(ttl=300)
def load_image(image_name: str):
    """Displays an image.

    Parameters
    ----------
    image_name : str
        Local path of the image.

    Returns
    -------
    Image
        Image to be displayed.
    """
    return Image.open(f"whitebox/streamlit/references/{image_name}")


def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
