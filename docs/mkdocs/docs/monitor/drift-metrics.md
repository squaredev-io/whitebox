# Drift metrics

The target of drift metrics is to calculate the data drift between 2 datasets.quality of an machine learning model. Currently supported drift types are:

- Data drift
- Concept drift

## Data drift

An analysis happens comparing the current data to the reference data estimating the distributions of each feature in the two datasets. The schema of both datasets should be identical.

Returns a drift summary of the following form:

```
{'timestamp': the timestamp of the report,
 'drift_summary': 
    {'number_of_columns': total number of dataset columns,
     'number_of_drifted_columns': total number of drifted columns,
     'share_of_drifted_columns': ('number_of_drifted_columns/'number_of_columns'),
     'dataset_drift': Boolean based on the criteria below,
     'drift_by_columns': 
        {'column1': {'column_name': 'column1',
                     'column_type': the type of column (e.g. num),
                     'stattest_name': the statistical test tha was used,
                     'drift_score': the drifting score based on the test,
                     'drift_detected': Boolean based on the criteria below,
                     'threshold': a float number based on the criteria below}, 
                    {......}
        }
    }
}
```

Logic to choose the appropriate statistical test is based on:

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