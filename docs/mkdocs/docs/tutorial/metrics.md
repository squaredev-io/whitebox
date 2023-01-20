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
| **missing_count**      | `numerical` & `categorical` |
| **non_missing_count**  | `numerical` & `categorical` |
| **mean**               | `numerical`                 |
| **minimum**            | `numerical`                 |
| **maximum**            | `numerical`                 |
| **sum**                | `numerical`                 |
| **standard_deviation** | `numerical`                 |
| **variance**           | `numerical`                 |

## Drifting Metrics

**Requirements**:

- Inferences
- Training Dataset

!!! note

    If actuals aren't provided for all inferences, then **ONLY the inferences that have actuals** will be used for the calculation of the drifting metrics.

## Performance Evaluation Metrics

**Requirements**:

- Inferences
- Actuals for the inferences

The target of evaluation metrics is to evaluate the quality of an machine learning model. Currently supported models are:

- Binary classification
- Multi-class classification

| Metric               | Supported model                                        |
| -------------------- | ------------------------------------------------------ |
| **confusion matrix** | `binary classification` & `multi-class classification` |
| **accuracy**         | `binary classification` & `multi-class classification` |
| **precision**        | `binary classification` & `multi-class classification` |
| **recall**           | `binary classification` & `multi-class classification` |
| **f1 score**         | `binary classification` & `multi-class classification` |

## Explainability

**Requirements**:

- Inferences

The target of the explainability feature is to provide a contribution score of each feature to each individual prediction, in a try to explain how the model concluded in the specific prediction. To achieve this we define 3 Levels of confidence in the explainability feature, based on how accessible or not is the client's input:

- **Level-0**: In this level a replacement model is trained in the same training data as client's model, and used for the explainability feature.
- **Level-1** (_pending_): In this level a surrogate model is trained in a way of trying to achieve the same predictions as client's model, and used for the explainability feature.
- **Level-2** (_pending_): Client's model is used for the explainability feature.

### Level-0 confidence

At this level a replacement model is trained in the same training data as client's model, and used for the explainability feature. Below there is a table of used models per machine learning task.

| Model        | Task                                                   |
| ------------ | ------------------------------------------------------ |
| **LightGBM** | `binary classification` & `multi-class classification` |

The fine tuning of models, through a hyper-parameters exploration is a pending task for now.

The trained model along with the inference data are used as input in <a href="/glossary/metric-definitions/#local-interpretable-model-agnostic-explanations" class="external-link" target="_blank">LIME</a> library, and the below report is provided - presenting the contribution of each feature in a specific prediction (the report includes all the feature contribution score to an descending order based on the absolute score value):

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
