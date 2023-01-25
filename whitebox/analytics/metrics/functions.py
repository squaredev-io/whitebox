from sklearn.metrics import multilabel_confusion_matrix
import pandas as pd
from typing import Dict, Union, List


def format_feature_metrics(
    missing_count: Dict[str, int],
    non_missing_count: Dict[str, int],
    mean: Dict[str, float],
    minimum: Dict[str, float],
    maximum: Dict[str, float],
    sum: Dict[str, float],
    standard_deviation: Dict[str, float],
    variance: Dict[str, float],
) -> Dict[str, Union[int, float]]:
    formated_metrics = {
        "missing_count": missing_count,
        "non_missing_count": non_missing_count,
        "mean": mean,
        "minimum": minimum,
        "maximum": maximum,
        "sum": sum,
        "standard_deviation": standard_deviation,
        "variance": variance,
    }

    return formated_metrics


def format_evaluation_metrics_binary(
    accuracy: float,
    precision: float,
    recall: float,
    f1: float,
    tn: int,
    fp: int,
    fn: int,
    tp: int,
) -> Dict[str, Union[int, float]]:
    formated_metrics_for_binary = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "true_positive": tp,
    }

    return formated_metrics_for_binary


def format_evaluation_metrics_multiple(
    accuracy: float,
    precision_statistics: Dict[str, float],
    recall_statistics: Dict[str, float],
    f1_statistics: Dict[str, float],
    conf_matrix: Dict[str, Dict[str, int]],
) -> Dict[str, Union[float, Dict[str, Union[int, float]]]]:
    formated_metrics_for_multiple = {
        "accuracy": accuracy,
        "precision": precision_statistics,
        "recall": recall_statistics,
        "f1": f1_statistics,
        "confusion_matrix": conf_matrix,
    }

    return formated_metrics_for_multiple


def confusion_for_multiclass(
    test_set: pd.DataFrame, prediction_set: pd.DataFrame, labels: List[int]
) -> Dict[str, Dict[str, int]]:
    """
    Gets 2 datasets based on multiclass classification and calculates
    the corresponding confusion matrix outputs tn, fp, fn, tp

    Parameters
    ----------
    test_set : pd.DataFrame
        Multiclass ground truth labels.

    y_score : pd.DataFrame
        Multiclass predicted labels.

    Returns
    -------
    mult_dict : Dict

    """
    cm = multilabel_confusion_matrix(test_set, prediction_set, labels=labels)
    mult_dict = {}
    class_key = 0
    for i in cm:
        tn, fp, fn, tp = i.ravel()
        eval_dict = {
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
        }
        mult_dict["class{}".format(class_key)] = eval_dict
        class_key = class_key + 1
    return mult_dict
