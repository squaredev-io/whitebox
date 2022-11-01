import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from src.analytics.metrics.functions import *
from typing import Dict, Union, Any
import json
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def create_feature_metrics_pipeline(
    dataset: pd.DataFrame,
) -> Dict[str, Union[int, float]]:

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

    """
    Binary classification evaluation metrics

    Calculates the evaluation metrics for binary classification
    given two datasets

    Parameters
    ----------
    test_set : pd.DataFrame
        Given ground truth dataset

    prediction_set : pd.DataFrame
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
    f1 = recall = metrics.f1_score(test_set, prediction_set)
    tn, fp, fn, tp = confusion_matrix(test_set, prediction_set).ravel()

    return format_evaluation_metrics_binary(
        accuracy, precision, recall, f1, tn, fp, fn, tp
    )


def create_multiple_classification_evaluation_metrics_pipeline(
    test_set: pd.DataFrame, prediction_set: pd.DataFrame
) -> Dict[str, Union[float, Dict[str, Union[int, float]]]]:
    """
    Multiclass classification evaluation metrics

    Calculates the evaluation metrics for multiclass classification
    given two datasets

    Parameters
    ----------
    test_set : pd.DataFrame
        Given ground truth dataset

    prediction_set : pd.DataFrame
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
    conf_matrix = confusion_for_multiclass(test_set, prediction_set)

    return format_evaluation_metrics_multiple(
        accuracy, precision_statistics, recall_statistics, f1_statistics, conf_matrix
    )


def create_data_drift_pipeline(
    reference_dataset: pd.DataFrame, current_dataset: pd.DataFrame
) -> Dict[str, Any]:
    """
    Two datasets are needed
    The reference dataset serves as a benchmark.
    An analysis happens comparing the current production data to the reference data.

    The dataset should include the needed features to evaluate for drift.
    The schema of both datasets should be identical.
    - In the case of pandas DataFrame, all column names should be string
    - All feature columns analyzed for drift should have the numerical type (np.number)
    - Categorical data can be encoded as numerical labels and specified in the column_mapping.
    - DateTime column is the only exception. If available, it can be used as the x-axis in the plots.

    Potentially, any two datasets can be used for comparison. Only the reference dataset
    will be used as a basis for comparison.

    How it works

    To estimate the data drift Evidently compares the distributions of each feature in the two datasets.
    Evidently applies statistical tests to detect if the distribution has changed significantly. There is a default
    logic to choosing the appropriate statistical test based on:
    - feature type: categorical or numerical
    - the number of observations in the reference dataset
    - the number of unique values in the feature (n_unique)

    For small data with <= 1000 observations in the reference dataset:
    - For numerical features (n_unique > 5): two-sample Kolmogorov-Smirnov test.
    - For categorical features or numerical features with n_unique <= 5: chi-squared test.
    - For binary categorical features (n_unique <= 2), we use the proportion difference test for independent samples based on Z-score.

    All tests use a 0.95 confidence level by default.

    For larger data with > 1000 observations in the reference dataset:
    - For numerical features (n_unique > 5): Wasserstein Distance.
    - For categorical features or numerical with n_unique <= 5): Jensen–Shannon divergence.

    All tests use a threshold = 0.1 by default.

    """
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_dataset, current_data=current_dataset)

    initial_report = drift_report.json()
    initial_report = json.loads(initial_report)

    data_drift_report = {}
    data_drift_report["timestamp"] = initial_report["timestamp"]
    data_drift_report["drift_summary"] = initial_report["metrics"]["DataDriftTable"]

    return data_drift_report
