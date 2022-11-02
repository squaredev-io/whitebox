import pandas as pd
from typing import Dict, Union, Any
import json
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def create_data_drift_pipeline(
    reference_dataset: pd.DataFrame, current_dataset: pd.DataFrame
) -> Dict[str, Union[DataDriftPreset, str]]:
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
