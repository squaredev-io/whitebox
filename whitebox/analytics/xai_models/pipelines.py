import pandas as pd
from typing import Dict
import joblib
import lime
import lime.lime_tabular
from whitebox.analytics.models.pipelines import *
from whitebox.core.settings import get_settings


settings = get_settings()


def create_xai_pipeline_classification_per_inference_row(
    training_set: pd.DataFrame,
    target: str,
    inference_row: pd.Series,
    type_of_task: str,
    model_id: str,
) -> Dict[str, float]:

    model_base_path = settings.MODEL_PATH
    model_path = f"{model_base_path}/{model_id}"

    xai_dataset = training_set.drop(columns=[target])
    explainability_report = {}

    # Make a mapping dict which will be used later to map the explainer index
    # with the features names

    mapping_dict = {}
    for feature in range(0, len(xai_dataset.columns.tolist())):
        mapping_dict[feature] = xai_dataset.columns.tolist()[feature]

    # Expainability for both classifications tasks
    # We have again to revisit here in the future as in case we upload the model
    # from the file system we don't care if it is binary or multiclass

    if type_of_task == "multi_class":

        # Giving the option of retrieving the local model

        model = joblib.load(f"{model_path}/lgb_multi.pkl")
        explainer = lime.lime_tabular.LimeTabularExplainer(
            xai_dataset.values,
            feature_names=xai_dataset.columns.values.tolist(),
            mode="classification",
            random_state=1,
        )

        exp = explainer.explain_instance(inference_row, model.predict)
        med_report = exp.as_map()
        temp_dict = dict(list(med_report.values())[0])
        explainability_report = {
            mapping_dict[name]: val for name, val in temp_dict.items()
        }

    elif type_of_task == "binary":

        # Giving the option of retrieving the local model

        model = joblib.load(f"{model_path}/lgb_binary.pkl")
        explainer = lime.lime_tabular.LimeTabularExplainer(
            xai_dataset.values,
            feature_names=xai_dataset.columns.values.tolist(),
            mode="classification",
            random_state=1,
        )

        exp = explainer.explain_instance(inference_row, model.predict_proba)
        med_report = exp.as_map()
        temp_dict = dict(list(med_report.values())[0])
        explainability_report = {
            mapping_dict[name]: val for name, val in temp_dict.items()
        }

    return explainability_report
