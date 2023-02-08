# SDK Documentation

This is the documentation for Whitebox's SDK. For an interactive experience, you can expirement with the SDK's <a href="https://github.com/squaredev-io/whitebox/tree/main/examples/notebooks" class="external-link" target="_blank">Jupyter notebooks</a>.

## Models

**_create_model_**_(name, type, features, prediction, probability, labels=None, description="")_

Creates a model in the database. This model works as placeholder for all the actual model's metadata.

| Parameter       | Type                      | Description                                                                                                            |
| --------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **name**        | `str`                     | The name of the model.                                                                                                 |
| **type**        | `str`                     | The model's type. Possible values: `binary`, `multi_class`, `regression`.                                              |
| **features**    | `Dict[str, FeatureTypes]` | The model's features. Possible values for `FeatureTypes`: `categorical`, `boolean`, `string`, `datetime`, `numerical`. |
| **prediction**  | `str`                     | The prediction of the model.                                                                                           |
| **probability** | `str`                     | The probability of the model.                                                                                          |
| **labels**      | `Dict[str, int]`          | The model's labels. Defaults to `None`.                                                                                |
| **description** | `str`                     | The model's description. Defaults to an empty string `""`.                                                             |

!!! info

    Labels are not applicable ONLY in regression models.

**_get_model_**_(model_id)_

Fetches the model with the specified ID from the database.

| Parameter    | Type  | Description          |
| ------------ | ----- | -------------------- |
| **model_id** | `str` | The ID of the model. |

**_delete_model_**_(model_id)_

Deletes the model with the specified ID from the database.

| Parameter    | Type  | Description          |
| ------------ | ----- | -------------------- |
| **model_id** | `str` | The ID of the model. |

## Training Datasets

**_log_training_dataset_**_(model_id, non_processed, processed)_

Inserts a set of dataset rows into the database. When the dataset rows are successfully saved, the pipeline for training the model is triggered. Then, the trained model is saved in the `/models/your_model's_id` folder of whitebox's root directory.

| Parameter         | Type           | Description                         |
| ----------------- | -------------- | ----------------------------------- |
| **model_id**      | `str`          | The ID of the model.                |
| **non_processed** | `pd.DataFrame` | The non processed training dataset. |
| **processed**     | `pd.DataFrame` | The processed training dataset.     |

!!! info

    The non processed and processed dataframes must have the same length.

## Inferences

**_log_inferences_**_(model_id, non_processed, processed, timestamps, actuals=None)_

Inserts a set of inference rows into the database.

| Parameter         | Type           | Description                                                                         |
| ----------------- | -------------- | ----------------------------------------------------------------------------------- |
| **model_id**      | `str`          | The ID of the model.                                                                |
| **non_processed** | `pd.DataFrame` | The non processed inferences.                                                       |
| **processed**     | `pd.DataFrame` | The processed inferences.                                                           |
| **timestamps**    | `pd.Series`    | The timestamps for each inference row in the inference dataframes.                  |
| **actuals**       | `pd.Series`    | The actuals for each inference row in the inference dataframes. Defaults to `None`. |

!!! info

    The non processed and processed dataframes along with the timestamps and actuals series must **ALL** have the same length.

## Monitors

**_create_model_monitor_**_(model_id, name, status, metric, severity, email, feature=None, lower_threshold=None)_

Creates a monitor for a specific metric.

| Parameter           | Type             | Description                                                                                                                                                                                               |
| ------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **model_id**        | `str`            | The ID of the model.                                                                                                                                                                                      |
| **name**            | `str`            | The name of the monitor.                                                                                                                                                                                  |
| **status**          | `MonitorStatus`  | The status of the monitor. Possible values for `MonitorStatus`: `active`, `inactive`.                                                                                                                     |
| **metric**          | `MonitorMetrics` | The metric that will be monitored. Possible values for `MonitorMetrics`: `accuracy`, `precision`, `recall`, `f1`, `r_square`, `mean_squared_error`, `mean_absolute_error`, `data_drift`, `concept_drift`. |
| **severity**        | `AlertSeverity`  | The severity of the alert the monitor produces. Possible values for `AlertSeverity`: `low`, `mid`, `high`.                                                                                                |
| **email**           | `str`            | The email to which the alert will be sent.                                                                                                                                                                |
| **feature**         | `str`            | The feature to be monitored. Defaults to `None`.                                                                                                                                                          |
| **lower_threshold** | `float`          | The threshold below which an alert will be produced. Defaults to `None`.                                                                                                                                  |

!!! note

    Some metrics like the data drift don't use a threshold so the feature that will be monitored should be inserted. In any case, both `feature` and `lower_threshold` can't be `None` at the same time.
