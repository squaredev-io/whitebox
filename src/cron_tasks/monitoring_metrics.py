from datetime import datetime

from src import crud, entities
from src.analytics.drift.pipelines import run_data_drift_pipeline
from src.analytics.metrics.pipelines import (
    create_binary_classification_evaluation_metrics_pipeline,
    create_feature_metrics_pipeline,
    create_multiple_classification_evaluation_metrics_pipeline,
)
from src.core.db import SessionLocal
from src.core.settings import get_settings
from src.cron_tasks.shared import (
    get_all_models,
    get_model_dataset_rows_df,
    get_model_processed_inference_rows_df,
    get_model_inference_rows_df,
)
from src.schemas.model import ModelType
from src.schemas.modelIntegrityMetric import ModelIntegrityMetricCreate

settings = get_settings()
db = SessionLocal()


async def run_calculate_drifting_metrics_pipeline():
    """
    Run the pipeline to calculate the drifting metrics
    After the metrics are calculated they are sabved in the database
    """
    models = await get_all_models(db)

    for model in models:
        inference_df = await get_model_processed_inference_rows_df(
            db, model_id=model.id
        )
        training_df = await get_model_dataset_rows_df(db, model_id=model.id)

        data_drif_report = run_data_drift_pipeline(training_df, inference_df)
        # TODO: Fix pipeline to return a DataDriftTable first

        new_drifting_metric = entities.DriftingMetric(
            timestamp=str(datetime.utcnow()),
            model_id=model.id,
            data_drift_summary=data_drif_report,
        )

        crud.drifting_metrics.create(db, obj_in=new_drifting_metric)


async def run_calculate_performance_metrics_pipeline():
    """
    Run the pipeline to calculate the perfomance metrics
    After the metrics are calculated they are saved in the database
    """
    models = await get_all_models(db)

    for model in models:
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
            print("multi class ----------------")

            print(processed_df)

            print(actual_df)
            multiclass_classification_metrics_report = (
                create_multiple_classification_evaluation_metrics_pipeline(
                    actual_df, processed_df
                )
            )

            print(multiclass_classification_metrics_report)

            new_performance_metric = entities.MultiClassificationMetrics(
                model_id=model.id,
                timestamp=str(datetime.utcnow()),
                **multiclass_classification_metrics_report
            )

            crud.multi_classification_metrics.create(db, obj_in=new_performance_metric)


async def run_calculate_feature_metrics_pipeline():
    """
    Run the pipeline to calculate the feature metrics
    After the metrics are calculated they are saved in the database
    """
    models = await get_all_models(db)

    for model in models:
        processed_df, nonprocessed_df, actual_df = await get_model_inference_rows_df(
            db, model_id=model.id
        )

        feature_metrics_report = create_feature_metrics_pipeline(processed_df)

        if feature_metrics_report:
            new_feature_metric = dict(
                model_id=model.id,
                timestamp=str(datetime.utcnow()),
                feature_metrics = feature_metrics_report
            )

            crud.model_integrity_metrics.create(db, obj_in=ModelIntegrityMetricCreate(**new_feature_metric))
