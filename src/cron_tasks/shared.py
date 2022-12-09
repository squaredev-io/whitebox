from typing import List, Union

import pandas as pd
from sqlalchemy.orm import Session

from src import crud
from src.schemas.model import Model, ModelType
from src.schemas.modelMonitor import ModelMonitor
from src.schemas.driftingMetric import DriftingMetric
from src.schemas.performanceMetric import (
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


async def get_model_processed_inference_rows_df(
    db: Session, model_id: str
) -> pd.DataFrame:
    inference_rows_in_db = crud.inference_rows.get_inference_rows_by_model(
        db=db, model_id=model_id
    )
    inference_rows_processed = [x.processed for x in inference_rows_in_db]
    inference_df = pd.DataFrame(inference_rows_processed)
    return inference_df


async def get_model_inference_rows_df(
    db: Session, model_id: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    inference_rows_in_db = crud.inference_rows.get_inference_rows_by_model(
        db=db, model_id=model_id
    )
    inference_rows_processed = [x.processed for x in inference_rows_in_db]
    inference_rows_nonprocessed = [x.nonprocessed for x in inference_rows_in_db]
    inference_rows_actual = [x.actual for x in inference_rows_in_db]
    processed_df = pd.DataFrame(inference_rows_processed)
    nonprocessed_df = pd.DataFrame(inference_rows_nonprocessed)
    actual_df = pd.Series(inference_rows_actual)

    # TODO: check if the length of the dataframes is the same
    return processed_df, nonprocessed_df, actual_df


async def get_all_models(db: Session) -> List[Model]:
    models_in_db = crud.models.get_all(db)
    return models_in_db


async def get_model_monitors(db: Session, model_id: str) -> List[ModelMonitor]:
    model_monitors_in_db = crud.model_monitors.get_model_monitors_by_model(
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
    else:
        last_report_in_db = (
            crud.multi_classification_metrics.get_latest_report_by_model(
                db, model_id=model.id
            )
        )
    return last_report_in_db


async def get_latest_data_drift_metrics_report(
    db: Session, model: Model
) -> DriftingMetric:
    last_report_in_db = crud.drifting_metrics.get_latest_report_by_model(
        db, model_id=model.id
    )
    return last_report_in_db
