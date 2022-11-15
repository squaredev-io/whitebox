from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from src.crud.dataset_rows import dataset_rows
from src.crud.inference_rows import inference_rows
from src.crud.models import models
from src.schemas.model import Model


async def get_model_dataset_rows_df(db: Session, model_id: str) -> pd.DataFrame:
    dataset_rows_in_db = dataset_rows.get_dataset_rows(db=db, model_id=model_id)
    dataset_rows_processed = [x.processed for x in dataset_rows_in_db]
    dataset_df = pd.DataFrame(dataset_rows_processed)
    return dataset_df


async def get_model_processed_inference_rows_df(
    db: Session, model_id: str
) -> pd.DataFrame:
    inference_rows_in_db = inference_rows.get_model_inference_rows(
        db=db, model_id=model_id
    )
    inference_rows_processed = [x.processed for x in inference_rows_in_db]
    inference_df = pd.DataFrame(inference_rows_processed)
    return inference_df


async def get_model_inference_rows_df(
    db: Session, model_id: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    inference_rows_in_db = inference_rows.get_model_inference_rows(
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
    models_in_db = models.get_all(db)
    return models_in_db
