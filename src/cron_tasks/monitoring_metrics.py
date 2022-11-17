from datetime import datetime
import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src import crud, entities
from src.analytics.drift.pipelines import run_data_drift_pipeline
from src.analytics.metrics.pipelines import (
    create_binary_classification_evaluation_metrics_pipeline,
    create_feature_metrics_pipeline,
    create_multiple_classification_evaluation_metrics_pipeline,
)
from src.core.settings import get_settings
from src.cron_tasks.shared import (
    get_all_models,
    get_model_dataset_rows_df,
    get_model_processed_inference_rows_df,
    get_model_inference_rows_df,
)
from src.schemas.model import Model, ModelType
from src.schemas.modelIntegrityMetric import ModelIntegrityMetricCreate
from src.utils.logger import cronLogger as logger


settings = get_settings()

engine = create_engine(settings.POSTGRES_DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


async def run_calculate_drifting_metrics_pipeline(
    model: Model, processed_inference_df: pd.DataFrame
):
    """
    Run the pipeline to calculate the drifting metrics
    After the metrics are calculated they are sabved in the database
    """

    processed_training_df = await get_model_dataset_rows_df(db, model_id=model.id)

    if processed_inference_df.empty or processed_training_df.empty:
        logger.info(f"Can't calculate data drift metrics for model {model.id}")
        return

    logger.info(f"Calculating drifting metrics for model {model.id}...")

    # We need to drop the target column from the data to calculate drfitting metrics
    processed_inference_dropped_target_df = processed_inference_df.drop(
        [model.prediction], axis=1
    )
    processed_training_dropped_target_df = processed_training_df.drop(
        [model.prediction], axis=1
    )

    data_drif_report = run_data_drift_pipeline(
        processed_training_dropped_target_df, processed_inference_dropped_target_df
    )

    new_drifting_metric = entities.DriftingMetric(
        timestamp=str(datetime.utcnow()),
        model_id=model.id,
        data_drift_summary=data_drif_report,
    )

    crud.drifting_metrics.create(db, obj_in=new_drifting_metric)
    logger.info("Drifting metrics calcutated!")


async def run_calculate_performance_metrics_pipeline(
    model: Model, processed_df: pd.DataFrame, actual_df: pd.DataFrame
):
    """
    Run the pipeline to calculate the perfomance metrics
    After the metrics are calculated they are saved in the database
    """

    if actual_df.empty:
        logger.info(
            f"Can't calculate performance metrics for model {model.id} because no actuals were found!"
        )
        return

    logger.info(f"Calculating performance metrics for model {model.id}")
    if model.type == ModelType.binary:
        binary_classification_metrics_report = (
            create_binary_classification_evaluation_metrics_pipeline(
                actual_df, processed_df[model.prediction]
            )
        )

        new_performance_metric = entities.BinaryClassificationMetrics(
            model_id=model.id,
            timestamp=str(datetime.utcnow()),
            **dict(binary_classification_metrics_report),
        )

        crud.binary_classification_metrics.create(db, obj_in=new_performance_metric)

    elif model.type == ModelType.multi_class:
        multiclass_classification_metrics_report = (
            create_multiple_classification_evaluation_metrics_pipeline(
                actual_df, processed_df[model.prediction]
            )
        )

        new_performance_metric = entities.MultiClassificationMetrics(
            model_id=model.id,
            timestamp=str(datetime.utcnow()),
            **dict(multiclass_classification_metrics_report),
        )

        crud.multi_classification_metrics.create(db, obj_in=new_performance_metric)

    logger.info("Performance metrics calcutated!")


async def run_calculate_feature_metrics_pipeline(
    model: Model, processed_df: pd.DataFrame
):
    """
    Run the pipeline to calculate the feature metrics
    After the metrics are calculated they are saved in the database
    """

    if processed_df.empty:
        logger.info(f"No inferences found for model {model.id}!")
        return

    logger.info(f"Calculating feature metrics for model {model.id}")
    feature_metrics_report = create_feature_metrics_pipeline(processed_df)

    if feature_metrics_report:
        new_feature_metric = ModelIntegrityMetricCreate(
            model_id=model.id,
            timestamp=str(datetime.utcnow()),
            feature_metrics=feature_metrics_report,
        )

        crud.model_integrity_metrics.create(db, obj_in=new_feature_metric)
        logger.info("Feature metrics calcutated!")


async def run_calculate_metrics_pipeline():
    logger.info("Beginning Metrics pipeline for all models!")
    start = time.time()
    engine.connect()

    models = await get_all_models(db)
    if not models:
        logger.info("No models found! Skipping pipeline")
    else:
        for model in models:
            (
                processed_df,
                nonprocessed_df,
                actual_df,
            ) = await get_model_inference_rows_df(db, model_id=model.id)
            if processed_df.empty:
                logger.info(
                    f"No inferences found for model {model.id}! Continuing with next model..."
                )
                continue
            logger.info(f"Executing Metrics pipeline for model {model.id}...")
            await run_calculate_drifting_metrics_pipeline(model, processed_df)

            await run_calculate_performance_metrics_pipeline(
                model, processed_df, actual_df
            )

            await run_calculate_feature_metrics_pipeline(model, processed_df)

            logger.info(f"Ended Metrics pipeline for model {model.id}...")

    db.close()
    end = time.time()
    logger.info("Metrics pipeline ended for all models!")
    logger.info("Runtime of Metrics pipeline took {}".format(end - start))
