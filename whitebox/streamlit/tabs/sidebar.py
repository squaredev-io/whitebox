import streamlit as st
from utils.load import load_config, load_image
from utils.export import display_links


def create_sidebar(model_names):
    readme = load_config("config_readme.toml")
    # Markdown for seeting logi in the center
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

    st.sidebar.image(load_image("logo.png"), width=120)
    display_links(readme["links"]["repo"])

    st.sidebar.write(
        "Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes."
    )

    model_option = st.sidebar.selectbox(
        "Please select one of your models below and then press 'Ok':",
        model_names,
        help=readme["tooltips"]["model_option"],
    )
    button = st.sidebar.button("Ok")

    return model_option, button
