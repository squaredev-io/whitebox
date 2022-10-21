import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from src.analytics.metrics.functions import *
from typing import Dict, Union


def create_feature_metrics_pipeline(
    dataset: pd.DataFrame,
) -> Dict[str, Union[int, float]]:
    missing_count = dataset.isna().sum().to_dict()
    non_missing_count = dataset.notna().sum().to_dict()
    mean = dataset.mean(numeric_only=True).to_dict()
    minimum = dataset.min(numeric_only=True).to_dict()
    maximum = dataset.max(numeric_only=True).to_dict()
    sum = dataset.sum(numeric_only=True).to_dict()
    standard_deviation = dataset.std(numeric_only=True).to_dict()
    variance = dataset.var(numeric_only=True).to_dict()

    return format_feature_metrics(
        missing_count,
        non_missing_count,
        mean,
        minimum,
        maximum,
        sum,
        standard_deviation,
        variance,
    )


def create_binary_classification_evaluation_metrics_pipeline(
    test_set: pd.DataFrame, prediction_set: pd.DataFrame
) -> Dict[str, Union[int, float]]:
    accuracy = metrics.accuracy_score(test_set, prediction_set)
    precision = metrics.precision_score(test_set, prediction_set)
    recall = metrics.recall_score(test_set, prediction_set)
    f1 = recall = metrics.f1_score(test_set, prediction_set)
    tn, fp, fn, tp = confusion_matrix(test_set, prediction_set).ravel()

    return format_evaluation_metrics_binary(
        accuracy, precision, recall, f1, tn, fp, fn, tp
    )


def create_multiple_classification_evaluation_metrics_pipeline(
    test_set: pd.DataFrame, prediction_set: pd.DataFrame
) -> Dict[str, Union[float, Dict[str, Union[int, float]]]]:
    accuracy = metrics.accuracy_score(test_set, prediction_set)
    micro_precision = metrics.precision_score(test_set, prediction_set, average="micro")
    macro_precision = metrics.precision_score(test_set, prediction_set, average="macro")
    weighted_precision = metrics.precision_score(
        test_set, prediction_set, average="weighted"
    )
    precision_statistics = {
        "micro": micro_precision,
        "macro": macro_precision,
        "weighted": weighted_precision,
    }
    micro_recall = metrics.recall_score(test_set, prediction_set, average="micro")
    macro_recall = metrics.recall_score(test_set, prediction_set, average="macro")
    weighted_recall = metrics.recall_score(test_set, prediction_set, average="weighted")
    recall_statistics = {
        "micro": micro_recall,
        "macro": macro_recall,
        "weighted": weighted_recall,
    }
    micro_f1 = metrics.f1_score(test_set, prediction_set, average="micro")
    macro_f1 = metrics.f1_score(test_set, prediction_set, average="macro")
    weighted_f1 = metrics.f1_score(test_set, prediction_set, average="weighted")
    f1_statistics = {"micro": micro_f1, "macro": macro_f1, "weighted": weighted_f1}
    conf_matrix = confusion_for_multiclass(test_set, prediction_set)

    return format_evaluation_metrics_multiple(
        accuracy, precision_statistics, recall_statistics, f1_statistics, conf_matrix
    )
