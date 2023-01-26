# SDK Documentation

## Models

**_create_model_**_(name, type, features, prediction, probability, labels, description="")_

Creates a model in the database. This model works as placeholder for all the actual model's metadata.

| Parameter       | Type                      | Description                                                                                                           |
| --------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **name**        | `str`                     | The name of the model.                                                                                                |
| **type**        | `str`                     | The model's type. Possible values: `binary`,`multi_class`, `regression`.                                              |
| **features**    | `Dict[str, FeatureTypes]` | The model's features. Possible values for `FeatureTypes`: `categorical`,`boolean`, `string`, `datetime`, `numerical`. |
| **prediction**  | `str`                     | The prediction of the model.                                                                                          |
| **probability** | `str`                     | The probability of the model.                                                                                         |
| **labels**      | `Dict[str, int]`          | The model's labels.                                                                                                   |
| **description** | `str`                     | The model's description. Defaults to an empty string `""`.                                                            |

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
