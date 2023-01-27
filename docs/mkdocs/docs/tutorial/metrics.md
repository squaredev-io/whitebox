# Metrics Calculation

!!! info

    The metrics are automatically calculated in a set interval for all models in the database.

    Depending on the data you have provided, the metrics calculation process will try to as many metrics possible for the specific model.

## Metric Requirements

All metrics require that inferences are provided for the specific model. If not, the whole process is skipped.
Each metric though has different requirements that need to be fulfilled in order to be calculated.
The requirements are listed in the following sections.

## Descriptive Statistics

The descriptive statistics are calculated per feature on any given dataset.

| Metric                 | Type of data                |
| ---------------------- | --------------------------- |
| **missing_count**      | `numerical` & `categorical` |
| **non_missing_count**  | `numerical` & `categorical` |
| **mean**               | `numerical`                 |
| **minimum**            | `numerical`                 |
| **maximum**            | `numerical`                 |
| **sum**                | `numerical`                 |
| **standard_deviation** | `numerical`                 |
| **variance**           | `numerical`                 |

## Drifting Metrics

The target of drift metrics is to calculate the data drift between 2 datasets. Currently supported drift types are:

- Data drift
- Concept drift

**Requirements**:

- Inferences
- Training Dataset

!!! note

    If actuals aren't provided for all inferences, then **ONLY the inferences that have actuals** will be used for the calculation of the drifting metrics.

### Data drift

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

### Concept drift

An analysis happens comparing the current target feature to the reference target feature.

Returns a concept drift summary of the following form:

```
{'timestamp': the timestamp of the report,
 'concept_drift_summary':
    {'column_name': 'column1',
     'column_type': the type of column (e.g. num),
     'stattest_name': the statistical test tha was used,
     'threshold': threshold used based on criteria below,
     'drift_score': the drifting score based on the test,
     'drift_detected': Boolean based on the criteria below,
    }
}
```

Logic to choose the appropriate statistical test is based on:

- the number of observations in the reference dataset
- the number of unique values in the target (n_unique)

For small data with <= 1000 observations in the reference dataset:

- For categorical target with n_unique > 2: chi-squared test.
- For binary categorical target (n_unique <= 2), we use the proportion difference test for independent samples based on Z-score.

All tests use a 0.95 confidence level by default.

For larger data with > 1000 observations in the reference dataset we use Jensen–Shannon divergence with a threshold = 0.1 .

## Performance Evaluation Metrics

**Requirements**:

- Inferences
- Actuals for the inferences

The target of evaluation metrics is to evaluate the quality of an machine learning model. Currently supported models are:

- Binary classification
- Multi-class classification
- Regression

| Metric                  | Supported model                                        |
| ----------------------- | ------------------------------------------------------ |
| **confusion matrix**    | `binary classification` & `multi-class classification` |
| **accuracy**            | `binary classification` & `multi-class classification` |
| **precision**           | `binary classification` & `multi-class classification` |
| **recall**              | `binary classification` & `multi-class classification` |
| **f1 score**            | `binary classification` & `multi-class classification` |
| **r_square**            | `regression`                                           |
| **mean_squared_error**  | `regression`                                           |
| **mean_absolute_error** | `regression`                                           |

## Explainability

**Requirements**:

- Inferences

The target of the explainability feature is to provide a contribution score of each feature to each individual prediction, in a try to explain how the model concluded in the specific prediction. To achieve this we define 3 Levels of confidence in the explainability feature, based on how accessible or not is the client's input:

- **Level-0**: In this level a replacement model is trained in the same training data as client's model, and used for the explainability feature.
- **Level-1** (_pending_): In this level a surrogate model is trained in a way of trying to achieve the same predictions as client's model, and used for the explainability feature.
- **Level-2** (_pending_): Client's model is used for the explainability feature.

### Level-0 confidence

At this level a replacement model is trained in the same training data as client's model, and used for the explainability feature. Below there is a table of used models per machine learning task.

| Model        | Task                                                                  |
| ------------ | --------------------------------------------------------------------- |
| **LightGBM** | `binary classification` & `multi-class classification` & `regression` |

The fine tuning of models, through a hyper-parameters exploration is a pending task for now.

The trained model along with the inference data are used as input in [LIME](../../metric-definitions/#local-interpretable-model-agnostic-explanations) library, and the below report is provided - presenting the contribution of each feature in a specific prediction (the report includes all the feature contribution score to an descending order based on the absolute score value):

```json
{
  "feature1": "contribution score",
  "feature2": "contribution score",
  "feature3": "contribution score"
}
```

### Level-1 confidence

Coming soon

### Level-2 confidence

Coming soon
