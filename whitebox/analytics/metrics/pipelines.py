import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from whitebox.analytics.metrics.functions import *
from typing import Dict, Union, Any, List
from whitebox.schemas.performanceMetric import (
    BinaryClassificationMetricsPipelineResult,
    MultiClassificationMetricsPipelineResult,
)
from whitebox.schemas.modelIntegrityMetric import FeatureMetrics


def create_feature_metrics_pipeline(
    dataset: pd.DataFrame,
) -> FeatureMetrics:

    """
    Feature metrics basic calculation

    Calculates the basic metrics of a given dataset

    Parameters
    ----------
    dataset : pd.DataFrame
        Given dataset for the calculation of metrics

    Returns
    -------
    feature_metrics : Dict

        The returned metrics are:
            missing_count,
            non_missing_count,
            mean,
            minimum,
            maximum,
            sum,
            standard_deviation,
            variance

    """
    missing_count = dataset.isna().sum().to_dict()
    non_missing_count = dataset.notna().sum().to_dict()
    mean = dataset.mean(numeric_only=True).to_dict()
    minimum = dataset.min(numeric_only=True).to_dict()
    maximum = dataset.max(numeric_only=True).to_dict()
    sum = dataset.sum(numeric_only=True).to_dict()
    standard_deviation = dataset.std(numeric_only=True).to_dict()
    variance = dataset.var(numeric_only=True).to_dict()

    return FeatureMetrics(
        **format_feature_metrics(
            missing_count,
            non_missing_count,
            mean,
            minimum,
            maximum,
            sum,
            standard_deviation,
            variance,
        )
    )


def create_binary_classification_evaluation_metrics_pipeline(
    test_set: pd.Series, prediction_set: pd.Series, labels: List[int]
) -> BinaryClassificationMetricsPipelineResult:

    """
    Binary classification evaluation metrics

    Calculates the evaluation metrics for binary classification
    given two datasets

    Parameters
    ----------
    test_set : pd.Series
        Given ground truth dataset

    prediction_set : pd.Series
        Given predictions dataset

    Returns
    -------
    evaluation_metrics : Dict

        The returned metrics are:
            accuracy,
            precision,
            recall,
            f1,
            tn,
            fp,
            fn,
            tp

    """

    accuracy = metrics.accuracy_score(test_set, prediction_set)
    precision = metrics.precision_score(test_set, prediction_set)
    recall = metrics.recall_score(test_set, prediction_set)
    f1 = metrics.f1_score(test_set, prediction_set)
    tn, fp, fn, tp = confusion_matrix(test_set, prediction_set, labels=labels).ravel()

    return BinaryClassificationMetricsPipelineResult(
        **format_evaluation_metrics_binary(
            accuracy, precision, recall, f1, tn, fp, fn, tp
        )
    )


def create_multiple_classification_evaluation_metrics_pipeline(
    test_set: pd.Series, prediction_set: pd.Series, labels: List[int]
) -> MultiClassificationMetricsPipelineResult:
    """
    Multiclass classification evaluation metrics

    Calculates the evaluation metrics for multiclass classification
    given two datasets

    Parameters
    ----------
    test_set : pd.Series
        Given ground truth dataset

    prediction_set : pd.Series
        Given predictions dataset

    Returns
    -------
    evaluation_metrics : Dict

        The returned metrics are:

            accuracy,

            precision_statistics
                micro_precision,
                macro_precision,
                weighted_precision,

            recall
                micro_recall,
                macro_recall,
                weighted_recall,

            f1
                micro_f1,
                macro_f1,
                weighted_f1

            conf_matrix
                tn,
                fp,
                fn,
                tp
    """
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
    conf_matrix = confusion_for_multiclass(test_set, prediction_set, labels)

    return MultiClassificationMetricsPipelineResult(
        **format_evaluation_metrics_multiple(
            accuracy,
            precision_statistics,
            recall_statistics,
            f1_statistics,
            conf_matrix,
        )
    )


def create_regression_evaluation_metrics_pipeline(
    test_set: pd.Series, prediction_set: pd.Series
) -> Dict[str, float]:

    """
    Regression evaluation metrics

    Calculates the evaluation metrics for regression
    given two datasets

    Parameters
    ----------
    test_set : pd.Series
        Given ground truth dataset

    prediction_set : pd.Series
        Given predictions dataset

    Returns
    -------
    evaluation_metrics : Dict

        The returned metrics are:
            r square,
            mean square error,
            mean absolute error

    """

    rsq = round(metrics.r2_score(test_set, prediction_set), 4)
    mse = round(metrics.mean_squared_error(test_set, prediction_set), 4)
    mae = round(metrics.mean_absolute_error(test_set, prediction_set), 4)

    regression_report = {}
    regression_report["r_square"] = rsq
    regression_report["mean_squared_error"] = mse
    regression_report["mean_absolute_error"] = mae

    return regression_report
