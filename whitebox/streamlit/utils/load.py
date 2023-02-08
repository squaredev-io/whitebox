import streamlit as st
from typing import Tuple, Dict, Any
import toml
from pathlib import Path
from PIL import Image


@st.cache(allow_output_mutation=True, ttl=300)
def load_config(config_readme_filename: str) -> Dict[Any, Any]:
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
    config_readme = toml.load(Path(f"streamlit/config/{config_readme_filename}"))
    return dict(config_readme)


@st.cache(ttl=300)
def load_image(image_name: str) -> Image:
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
    return Image.open(f"streamlit/references/{image_name}")
