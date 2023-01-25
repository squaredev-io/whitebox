# Using Whitebox SDK

## Installation

Installing Whitebox is a pretty easy job. Just install it like any other python package:

<div class="termy">

```console
$  pip install whitebox
```

</div>

All the required packages will be automatically installed!

Now you're good to go!

## Initial Setup

In order to run Whitebox, you will need the application's API key.
This key will be produced for you during the initial run of the Uvicorn live server.
Assuming you run the server with docker compose (you can find more in the install page of the tutorial), you will see the following output:

<div class="termy">

```console
$ docker compose up

...
<span style="color: green;">INFO</span>: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>: Started reloader process [4450] using StatReload
<span style="color: green;">INFO</span>: Started server process [4452]
<span style="color: green;">INFO</span>: Waiting for application startup.
<span style="color: green;">INFO</span>: Created username: admin, API key: some_api_key
<span style="color: green;">INFO</span>: Application startup complete.
...
```

</div>

!!! info

    Keep this API key somewhere safe!

    If you lose it, you will need to delete the admin user in your database and re-run the live serve to produce a new key!

After you get the API key, all you have to do is create an instance of the Whitebox class adding your host and API key as parameters:

```Python
from whitebox import Whitebox

wb = Whitebox(host="127.0.0.1:8000", api_key="some_api_key")
```

Now you're ready to start using Whitebox!

## Models

### Creating a Model

In order to start adding training datasets and inferences, you first need to create a model.

Let's create a sample model:

```Python
wb.create_model(
    name="Model 1",
    type="binary",
    features={
        'additionalProp1': 'numerical',
        'additionalProp2': 'numerical',
        'additionalProp3': 'numerical'
    },
    labels={
        'additionalProp1': 0,
        'additionalProp2': 1
    },
    prediction="target",
    probability="proba"
)
```

For more details about the schema accepted property types visit the <a href="/sdk-docs/#models" class="external-link" target="_blank">Models section</a> in the SDK documentation.

### Fetching a Model

Getting a model from the database is as easy as it sounds. You'll just need the `model_id`:

```Python
wb.get_model("some_model_id")
```

### Deleting a model

Deleting a model is as easy as fetching a model. Just use the `model_id`:

```Python
wb.delete_model("some_model_id")
```

!!! warning

    You will have to be extra careful when deleting a model because all datasets, inferences, monitors and literally everything will be deleted from the database along with the model itself!

## Loading Training Datasets

Once you have created a model you can start loading your data. Let's start with the training dataset!

In our example we will create a `pd.DataFrame` from a `.csv` file. Of course you can use any method you like to create your `pd.DataFrame` as long as your non-processed and processed datasets have **the same amount of rows** (a.k.a. the same length) and there are **more than one rows**!

```Python
import pandas as pd
non_processed_df = pd.read_csv("path/to/file/non_processed_data.csv")
processed_df = pd.read_csv("path/to/file/processed_data.csv")

wb.log_training_dataset(
    model_id="some_model_id",
    non_processed=non_processed_df,
    processed=processed_df
)
```

!!! note

    When your training dataset is saved in the database, the model training process will begin excecuting, based on this dataset and the model it's associated with. That's why you need to load all the rows of your training dataset in the same batch.

## Loading Inferences

To load your inferences you have to follow the exact same procedure as with the training datasets. The only difference is that you need to provide a `pd.Series` with the timestamps and (optionally) a `pd.Series` with the actuals, whose indices should match the ones in the non-processed and processed `pd.DataFrames`.

In our example let's assume that both the non-processed and processed `pd.DataFrames` have 10 rows each:

```Python
import pandas as pd
non_processed_df = pd.read_csv("path/to/file/non_processed_data.csv")
processed_df = pd.read_csv("path/to/file/processed_data.csv")

# Timestamps and actuals should have a length of 10
timestamps = pd.Series(["2022-12-22T12:13:27.879738"] * 10)
actuals = pd.Series([0, 1, 1, 1, 0, 0, 1, 1, 0, 0])

wb.log_inferences(
    model_id="some_model_id",
    non_processed=non_processed_df,
    processed=processed_df,
    timestamps=timestamps,
    actuals=actuals
)
```

!!! warning

    Make sure you add the actuals if you already know them, because as of now, there's no ability to add them at a later time by updating the inference rows.
