from datetime import datetime
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
# from src.core.db import SessionLocal

settings = get_settings()
# db = SessionLocal()

engine = create_engine(settings.POSTGRES_DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


async def run_calculate_drifting_metrics_pipeline(model: Model):
    """
    Run the pipeline to calculate the drifting metrics
    After the metrics are calculated they are sabved in the database
    """

    inference_df = await get_model_processed_inference_rows_df(
        db, model_id=model.id
    )
    training_df = await get_model_dataset_rows_df(db, model_id=model.id)

    if inference_df.empty or training_df.empty:
        logger.info(f"Can't calculate data drift metrics for model {model.id}")
        return

    logger.info(f"Calculating drifting metrics for model {model.id}...")

    data_drif_report = run_data_drift_pipeline(training_df, inference_df)

    new_drifting_metric = entities.DriftingMetric(
        timestamp=str(datetime.utcnow()),
        model_id=model.id,
        data_drift_summary=data_drif_report,
    )

    crud.drifting_metrics.create(db, obj_in=new_drifting_metric)
    logger.info("Drifting metrics calcutated!")


async def run_calculate_performance_metrics_pipeline(model: Model):
    """
    Run the pipeline to calculate the perfomance metrics
    After the metrics are calculated they are saved in the database
    """

    processed_df, nonprocessed_df, actual_df = await get_model_inference_rows_df(
        db, model_id=model.id
    )

    # feature_metrics_report = create_feature_metrics_pipeline(inference_df)

    # if model.type == ModelType.binary:
    #     binary_classification_metrics_report = (
    #         create_binary_classification_evaluation_metrics_pipeline(
    #             inference_df['actual'], inference_df['actual']
    #         )
    #     )

    if model.type == ModelType.multi_class:
        multiclass_classification_metrics_report = (
            create_multiple_classification_evaluation_metrics_pipeline(
                processed_df["y_testing_multi"], processed_df["y_prediction_multi"]
            )
        )

        new_performance_metric = entities.MultiClassificationMetrics(
            model_id=model.id,
            timestamp=str(datetime.utcnow()),
            **dict(multiclass_classification_metrics_report)
        )

        crud.multi_classification_metrics.create(db, obj_in=new_performance_metric)


async def run_calculate_feature_metrics_pipeline(model: Model):
    """
    Run the pipeline to calculate the feature metrics
    After the metrics are calculated they are saved in the database
    """

    processed_df, nonprocessed_df, actual_df = await get_model_inference_rows_df(
        db, model_id=model.id
    )

    if processed_df.empty:
        logger.info(f"No inferences found for model {model.id}!")
        return

    logger.info(f"Calculating feature metrics for model {model.id}")
    feature_metrics_report = create_feature_metrics_pipeline(processed_df)

    if feature_metrics_report:
        new_feature_metric = ModelIntegrityMetricCreate(
            model_id=model.id,
            timestamp=str(datetime.utcnow()),
            feature_metrics = feature_metrics_report
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
            logger.info(f"Executing Metrics pipeline for model {model.id}...")
            await run_calculate_drifting_metrics_pipeline(model)

            logger.info("Calculating performance metrics...")
            await run_calculate_performance_metrics_pipeline(model)
            logger.info("Performance metrics calcutated!")

            await run_calculate_feature_metrics_pipeline(model)

            logger.info(f"Ended Metrics pipeline for model {model.id}...")

    db.close()
    end = time.time()
    logger.info("Runtime of Metrics pipeline took {}".format(end - start))
