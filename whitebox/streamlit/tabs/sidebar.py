import streamlit as st
from utils.load import load_config, load_image, local_css
from utils.export import display_links, center_image
from typing import List, Tuple, Union, Dict, Any
from whitebox.schemas.model import Model
from whitebox import Whitebox
from utils.transformation import get_models_names, get_model_from_name


@st.cache_resource
def initialise_whitebox(host_option, api_key_option):
    wb = Whitebox(
        host=host_option,
        api_key=api_key_option,
    )
    return wb


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
    # Setup basic structure parts
    readme = load_config("config_readme.toml")
    center_image()
    st.sidebar.image(load_image("logo.png"), width=120)
    display_links(readme["links"]["repo"])
    st.sidebar.write(
        "Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes."
    )

    # Structure sidebar's additional expander sections
    local_css("whitebox/streamlit/utils/style.css")
    settings_expander = st.sidebar.expander("Settings", expanded=True)

    with settings_expander:
        host_option = st.text_input(
            "Paste here your host url:",
            max_chars=21,
            placeholder="http://127.0.0.1:8000",
            value="http://127.0.0.1:8000",
            help=readme["tooltips"]["host"],
        )

        api_key_option = st.text_input(
            "Paste here your api key:",
            max_chars=64,
            type="password",
            placeholder="your api key",
            help=readme["tooltips"]["api_key"],
        )
        setting_confirmation = st.checkbox("I'm ok, proceed with the above settings")

    # Initialise the other expanders only when the settings are confirmed
    if setting_confirmation:
        wb = initialise_whitebox(host_option, api_key_option)

        creation_model_expander = st.sidebar.expander("Create model", expanded=False)
        with creation_model_expander:
            create_new_model(wb, readme)

        selection_model_expander = st.sidebar.expander("Select model", expanded=False)
        with selection_model_expander:
            models_list = wb.get_models()
            model_names = get_models_names(models_list)
            model_option = st.selectbox(
                "Please select one of the found models below to be visualised:",
                model_names,
                help=readme["tooltips"]["model_option"],
            )

        modification_model_expander = st.sidebar.expander("Edit model", expanded=False)
        with modification_model_expander:
            st.write(f"This step will modify the selected model '{model_option}'")
            modify_selected_model(wb, models_list, readme, model_option)

        return model_option, models_list, setting_confirmation, wb
    else:
        return None, None, False, None


def create_new_model(wb: Whitebox, readme: Dict[str, Any]):
    model_name = st.text_input(
        "Enter your model name:",
        max_chars=25,
        placeholder="Your model name",
        help=readme["tooltips"]["model_name"],
    )

    description_name = st.text_input(
        "Enter your model description:",
        max_chars=25,
        placeholder="Your model description",
        help=readme["tooltips"]["model_description"],
    )

    model_type_option = create_model_type_select_box(readme, "type_create")

    prediction_column_name = st.text_input(
        "Enter your target column name",
        max_chars=10,
        placeholder="Your target column name",
        help=readme["tooltips"]["target_column"],
    )
    create_model_button = st.button("Create model")

    if create_model_button:
        # Have a control for geting both model name and target column name
        if (len(model_name) > 0) & (len(prediction_column_name) > 0):
            wb.create_model(
                name=model_name,
                description=description_name,
                type=model_type_option,
                prediction=prediction_column_name,
            )
            st.write("The new model has been created!")


def create_model_type_select_box(readme: Dict[str, Any], key: str):
    model_type_option_list = ["binary", "multi_class", "regression"]
    model_type_option = st.selectbox(
        "Please select one of the found models below:",
        model_type_option_list,
        help=readme["tooltips"]["model_type"],
        key=key,
    )
    return model_type_option


def update_model_attribute(
    wb: Whitebox, model_id: str, selected_attribute: str, value: str
):
    updated_model = wb.update_model(model_id, {selected_attribute: value})
    st.write(f"Updated the selected model '{selected_attribute}'!")

    return updated_model


def modify_selected_model(
    wb: Whitebox,
    models_list: Union[List[Model], None],
    readme: Dict[str, Any],
    selected_model_name: str,
):
    # Get the id of the previous selected model
    selected_model = get_model_from_name(models_list, selected_model_name)
    model_id = selected_model["id"]

    model_option = st.selectbox(
        "Please select one of the below options:",
        [
            "delete model",
            "rename model",
            "change model description",
            "change model type",
        ],
    )
    if model_option == "delete model":
        delete_button = st.button("Delete model")
        if delete_button:
            delete_model = wb.delete_model(model_id)
            st.write(f"Deleted model '{selected_model}'!")

    elif model_option == "rename model":
        new_name_value = st.text_input("Please provide below the new model name:")
        rename_button = st.button("Rename model")
        if rename_button:
            update_model_attribute(wb, model_id, "name", new_name_value)

    elif model_option == "change model description":
        new_description_value = st.text_input(
            "Please provide below the new model description:"
        )
        description_button = st.button("Change model description")
        if description_button:
            update_model_attribute(wb, model_id, "description", new_description_value)

    elif model_option == "change model type":
        new_type_value = create_model_type_select_box(readme, "type_change")
        type_button = st.button("Change model type")
        if type_button:
            update_model_attribute(wb, model_id, "type", new_type_value)
