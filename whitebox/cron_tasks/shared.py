from typing import Callable, Dict, List, Tuple, Union
import itertools
import pandas as pd
import datetime
import pytz
from sqlalchemy.orm import Session
from whitebox import crud
from whitebox.schemas.inferenceRow import InferenceRow
from whitebox.schemas.model import Model, ModelType
from whitebox.schemas.modelMonitor import ModelMonitor
from whitebox.schemas.driftingMetric import DriftingMetric
from whitebox.schemas.performanceMetric import (
    BinaryClassificationMetrics,
    MultiClassificationMetrics,
)


async def get_model_dataset_rows_df(db: Session, model_id: str) -> pd.DataFrame:
    dataset_rows_in_db = crud.dataset_rows.get_dataset_rows_by_model(
        db=db, model_id=model_id
    )
    dataset_rows_processed = [x.processed for x in dataset_rows_in_db]
    dataset_df = pd.DataFrame(dataset_rows_processed)
    return dataset_df


async def get_unused_model_inference_rows(
    db: Session, model_id: str
) -> List[InferenceRow]:
    return crud.inference_rows.get_unused_inference_rows(db=db, model_id=model_id)


async def group_inference_rows_by_timestamp(
    inference_rows: List[InferenceRow],
    last_time: datetime.datetime,
    granularity_amount: int,
    granularity_type: str,
) -> List[Dict[datetime.datetime, List[InferenceRow]]]:
    """Create a list of dicts with all inferences grouped by timestamp"""

    dict_inference_rows = [vars(x) for x in inference_rows]

    updated_inferences_dict = []
    for x in dict_inference_rows:
        new_obj = {**x}
        new_obj["timestamp"] = change_timestamp(
            x["timestamp"],
            last_time,
            granularity_amount,
            granularity_type,
        )
        updated_inferences_dict.append(new_obj)

    updated_inferences = [InferenceRow(**x) for x in updated_inferences_dict]

    key_func: Callable[[InferenceRow]] = lambda x: x.timestamp

    grouped_inferences = [
        {key: list(group)}
        for key, group in itertools.groupby(updated_inferences, key_func)
    ]

    return grouped_inferences


async def seperate_inference_rows(
    inference_rows: List[InferenceRow],
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    inference_rows_processed = [x.processed for x in inference_rows]
    inference_rows_nonprocessed = [x.nonprocessed for x in inference_rows]
    inference_rows_actual = [x.actual for x in inference_rows]
    processed_df = pd.DataFrame(inference_rows_processed)
    nonprocessed_df = pd.DataFrame(inference_rows_nonprocessed)
    actual_df = pd.Series(inference_rows_actual)

    # TODO: check if the length of the dataframes is the same
    return processed_df, nonprocessed_df, actual_df


async def set_inference_rows_to_used(db: Session, ids: List[str]) -> None:
    """Changes the "is_used" property of an inference row to True"""

    for id in ids:
        inference_to_update = crud.inference_rows.get(db=db, _id=id)
        crud.inference_rows.update(
            db=db, db_obj=inference_to_update, obj_in={"is_used": True}
        )


async def get_all_models(db: Session) -> List[Model]:
    models_in_db = crud.models.get_all(db)
    return models_in_db


async def get_active_model_monitors(db: Session, model_id: str) -> List[ModelMonitor]:
    model_monitors_in_db = crud.model_monitors.get_active_model_monitors_by_model(
        db=db, model_id=model_id
    )
    return model_monitors_in_db


async def get_latest_performance_metrics_report(
    db: Session, model: Model
) -> Union[BinaryClassificationMetrics, MultiClassificationMetrics]:
    if model.type == ModelType.binary:
        last_report_in_db = (
            crud.binary_classification_metrics.get_latest_report_by_model(
                db, model_id=model.id
            )
        )
    elif model.type == ModelType.multi_class:
        last_report_in_db = (
            crud.multi_classification_metrics.get_latest_report_by_model(
                db, model_id=model.id
            )
        )
    else:
        last_report_in_db = crud.regression_metrics.get_latest_report_by_model(
            db, model_id=model.id
        )
    return last_report_in_db


async def get_latest_drift_metrics_report(db: Session, model: Model) -> DriftingMetric:
    last_report_in_db = crud.drifting_metrics.get_latest_report_by_model(
        db, model_id=model.id
    )
    return last_report_in_db


def round_timestamp(
    timestamp: datetime.datetime, granularity_type: str
) -> datetime.datetime:
    """Rounds a timestamp depending on a given unit
    (e.g. if the unit is D (day) it converts 2023-03-03 12:33:25.34432 into 2023-03-03 00:00:00)
    """

    if granularity_type == "T":
        timestamp = timestamp.replace(second=0, microsecond=0)
    elif granularity_type == "H":
        timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
    else:
        timestamp = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

    return timestamp


def convert_granularity_to_secs(granularity_amount: int, granularity_type: str) -> int:
    """Converts a granularity into seconds (e.g. 1 day in 1 * 86400 = 86400 seconds)"""

    amount_of_seconds = {"T": 60, "H": 3600, "D": 86400, "W": 604800}

    return granularity_amount * amount_of_seconds[granularity_type]


def change_timestamp(
    timestamp: datetime.datetime,
    start_time: datetime.datetime,
    granularity_amount: int,
    granularity_type: str,
) -> datetime.datetime:
    """Converts a specific timestamp into it's group's timestamp based on the granularity and previous group timestamp.\n
    (E.g. a timestamp 2023-03-03 12:33:25.34432 when granularity is set to 2D and the previous group's timestamp is \
        2023-03-03 00:00:00 will be converted into 2023-03-05 00:00:00)"""

    timestamp_utc_timezone = timestamp.replace(tzinfo=pytz.UTC)
    timestamp_in_seconds = round_timestamp(
        timestamp_utc_timezone, granularity_type
    ).timestamp()

    granularity_in_seconds = convert_granularity_to_secs(
        granularity_amount, granularity_type
    )

    start_time_in_seconds = start_time.timestamp()

    time_difference = (
        timestamp_in_seconds - start_time_in_seconds
    ) // granularity_in_seconds

    new_timestamp_in_seconds = (
        time_difference + 1
    ) * granularity_in_seconds + start_time_in_seconds

    new_timestamp = datetime.datetime.fromtimestamp(
        new_timestamp_in_seconds
    ).astimezone(datetime.timezone.utc)

    return new_timestamp


def get_used_inference_for_reusage(
    db: Session,
    model_id: str,
    inferences: List[InferenceRow],
    start_time: datetime.datetime,
    granularity_amount: int,
    granularity_type: str,
) -> List[InferenceRow]:
    """Collects already used inference rows to be grouped with new rows of the same timestamp group and be \
        reused to create new reports."""

    timestamps = [x.timestamp for x in inferences]

    changed_timestamps = [
        change_timestamp(x, start_time, granularity_amount, granularity_type)
        for x in timestamps
    ]
    unique_timestamps = list(set(changed_timestamps))

    granularity_in_seconds = convert_granularity_to_secs(
        granularity_amount, granularity_type
    )

    all_used_inferences = []

    for timestamp in unique_timestamps:
        previous_timestamp = timestamp - datetime.timedelta(
            seconds=granularity_in_seconds
        )

        used_inferences_for_timestamp = (
            crud.inference_rows.get_inference_rows_betweet_dates(
                db=db,
                model_id=model_id,
                min_date=previous_timestamp,
                max_date=timestamp,
            )
        )

        all_used_inferences += used_inferences_for_timestamp

    return all_used_inferences
