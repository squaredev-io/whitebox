from datetime import datetime
import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.encoders import jsonable_encoder
from whitebox import crud, entities
from whitebox.analytics.drift.pipelines import (
    run_data_drift_pipeline,
    run_concept_drift_pipeline,
)
from whitebox.analytics.metrics.pipelines import (
    create_binary_classification_evaluation_metrics_pipeline,
    create_feature_metrics_pipeline,
    create_multiple_classification_evaluation_metrics_pipeline,
    create_regression_evaluation_metrics_pipeline,
)
from whitebox.core.settings import get_settings
from whitebox.cron_tasks.shared import (
    get_all_models,
    get_model_dataset_rows_df,
    get_unused_model_inference_rows,
    group_inference_rows_by_timestamp,
    seperate_inference_rows,
    set_inference_rows_to_used,
    get_latest_drift_metrics_report,
    round_timestamp,
    get_used_inference_for_reusage,
)
from whitebox.schemas.model import Model, ModelType
from whitebox.schemas.modelIntegrityMetric import ModelIntegrityMetricCreate
from whitebox.utils.logger import cronLogger as logger


settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


async def run_calculate_drifting_metrics_pipeline(
    model: Model, inference_processed_df: pd.DataFrame, timestamp: datetime
):
    """
    Run the pipeline to calculate the drifting metrics
    After the metrics are calculated they are saved in the database
    """

    training_processed_df = await get_model_dataset_rows_df(db, model_id=model.id)

    if training_processed_df.empty:
        logger.info(f"Can't calculate data drift metrics for model {model.id}")
        return

    logger.info(f"Calculating drifting metrics for model {model.id}...")

    # We need to drop the target column from the data to calculate drifting metrics
    processed_inference_dropped_target_df = inference_processed_df.drop(
        [model.target_column], axis=1
    )
    processed_training_dropped_target_df = training_processed_df.drop(
        [model.target_column], axis=1
    )

    data_drift_report = run_data_drift_pipeline(
        processed_training_dropped_target_df, processed_inference_dropped_target_df
    )
    concept_drift_report = run_concept_drift_pipeline(
        training_processed_df,
        inference_processed_df,
        model.target_column,
    )

    new_drifting_metric = entities.DriftingMetric(
        timestamp=str(timestamp),
        model_id=model.id,
        concept_drift_summary=concept_drift_report,
        data_drift_summary=data_drift_report,
    )

    existing_report = crud.drifting_metrics.get_first_by_filter(
        db=db, model_id=model.id, timestamp=timestamp
    )
    if existing_report:
        crud.drifting_metrics.update(
            db=db, db_obj=existing_report, obj_in=jsonable_encoder(new_drifting_metric)
        )
    else:
        crud.drifting_metrics.create(db, obj_in=new_drifting_metric)
    logger.info("Drifting metrics calculated!")


async def run_calculate_performance_metrics_pipeline(
    model: Model,
    inference_processed_df: pd.DataFrame,
    actual_df: pd.DataFrame,
    timestamp: datetime,
):
    """
    Run the pipeline to calculate the performance metrics
    After the metrics are calculated they are saved in the database
    """

    cleaned_actuals_df = actual_df.dropna()

    if cleaned_actuals_df.empty:
        logger.info(
            f"Can't calculate performance metrics for model {model.id} because no actuals were found!"
        )
        return

    if len(cleaned_actuals_df.index) != len(actual_df.index):
        logger.info(
            f"Performance metrics will be calculated only for a portion of rows for model: {model.id}\
                because actuals were not provided for all inference rows!"
        )
        inference_processed_df = inference_processed_df.iloc[cleaned_actuals_df.index]

    inference_processed_df = inference_processed_df.reset_index(drop=True)
    cleaned_actuals_df = cleaned_actuals_df.reset_index(drop=True)

    if model.type is not ModelType.regression:
        if not model.labels:
            logger.info(
                f"Can't calculate performance metrics for model {model.id} because labels are required for binary and multi_class models!"
            )
            return
        labels = list(model.labels.values())

    logger.info(f"Calculating performance metrics for model {model.id}")
    if model.type == ModelType.binary:
        binary_classification_metrics_report = (
            create_binary_classification_evaluation_metrics_pipeline(
                cleaned_actuals_df, inference_processed_df[model.target_column], labels
            )
        )

        new_performance_metric = entities.BinaryClassificationMetrics(
            model_id=model.id,
            timestamp=str(timestamp),
            **dict(binary_classification_metrics_report),
        )

        existing_report = crud.binary_classification_metrics.get_first_by_filter(
            db=db, model_id=model.id, timestamp=timestamp
        )
        if existing_report:
            crud.binary_classification_metrics.update(
                db=db,
                db_obj=existing_report,
                obj_in=jsonable_encoder(new_performance_metric),
            )
        else:
            crud.binary_classification_metrics.create(db, obj_in=new_performance_metric)

    elif model.type == ModelType.multi_class:
        multiclass_classification_metrics_report = (
            create_multiple_classification_evaluation_metrics_pipeline(
                cleaned_actuals_df, inference_processed_df[model.target_column], labels
            )
        )

        new_performance_metric = entities.MultiClassificationMetrics(
            model_id=model.id,
            timestamp=str(timestamp),
            **dict(multiclass_classification_metrics_report),
        )

        existing_report = crud.multi_classification_metrics.get_first_by_filter(
            db=db, model_id=model.id, timestamp=timestamp
        )
        if existing_report:
            crud.multi_classification_metrics.update(
                db=db,
                db_obj=existing_report,
                obj_in=jsonable_encoder(new_performance_metric),
            )
        else:
            crud.multi_classification_metrics.create(db, obj_in=new_performance_metric)

    elif model.type == ModelType.regression:
        regression_metrics_report = create_regression_evaluation_metrics_pipeline(
            cleaned_actuals_df, inference_processed_df[model.target_column]
        )

        new_performance_metric = entities.RegressionMetrics(
            model_id=model.id,
            timestamp=str(timestamp),
            **dict(regression_metrics_report),
        )

        existing_report = crud.regression_metrics.get_first_by_filter(
            db=db, model_id=model.id, timestamp=timestamp
        )
        if existing_report:
            crud.regression_metrics.update(
                db=db,
                db_obj=existing_report,
                obj_in=jsonable_encoder(new_performance_metric),
            )
        else:
            crud.regression_metrics.create(db, obj_in=new_performance_metric)

    logger.info("Performance metrics calculated!")


async def run_calculate_feature_metrics_pipeline(
    model: Model, inference_processed_df: pd.DataFrame, timestamp: datetime
):
    """
    Run the pipeline to calculate the feature metrics
    After the metrics are calculated they are saved in the database
    """

    logger.info(f"Calculating feature metrics for model {model.id}")
    feature_metrics_report = create_feature_metrics_pipeline(inference_processed_df)

    if feature_metrics_report:
        new_feature_metric = ModelIntegrityMetricCreate(
            model_id=model.id,
            timestamp=str(timestamp),
            feature_metrics=feature_metrics_report,
        )

        existing_report = crud.model_integrity_metrics.get_first_by_filter(
            db=db, model_id=model.id, timestamp=timestamp
        )
        if existing_report:
            crud.model_integrity_metrics.update(
                db=db,
                db_obj=existing_report,
                obj_in=jsonable_encoder(new_feature_metric),
            )
        else:
            crud.model_integrity_metrics.create(db, obj_in=new_feature_metric)

        logger.info("Feature metrics calculated!")


async def run_calculate_metrics_pipeline():
    logger.info("Beginning Metrics pipeline for all models!")
    start = time.time()
    engine.connect()

    models = await get_all_models(db)
    if not models:
        logger.info("No models found! Skipping pipeline")
    else:
        for model in models:
            granularity = model.granularity
            granularity_amount = int(granularity[:-1])
            granularity_type = granularity[-1]

            last_report = await get_latest_drift_metrics_report(db, model)

            # We need to get the last report's timestamp as a base of grouping unless there's no report produced.
            # In this case, the base timestamp is considered the "now" rounded to the day so the intervals start from midnight
            # e.g. 12:00, 12:15, 12:30, 12:45 and so on if granularity is 15T.
            last_report_time = (
                last_report.timestamp
                if last_report
                else round_timestamp(datetime.utcnow(), "1D")
            )

            unused_inference_rows_in_db = await get_unused_model_inference_rows(
                db, model_id=model.id
            )

            if len(unused_inference_rows_in_db) == 0:
                logger.info(
                    f"No new inferences found for model {model.id}! Continuing with next model..."
                )
                continue
            logger.info(f"Executing Metrics pipeline for model {model.id}...")

            used_inferences = get_used_inference_for_reusage(
                db,
                model.id,
                unused_inference_rows_in_db,
                last_report_time,
                granularity_amount,
                granularity_type,
            )

            all_inferences = unused_inference_rows_in_db + used_inferences

            grouped_inference_rows = await group_inference_rows_by_timestamp(
                all_inferences,
                last_report_time,
                granularity_amount,
                granularity_type,
            )

            for group in grouped_inference_rows:
                for timestamp, inference_group in group.items():
                    inference_rows_ids = [x.id for x in inference_group]
                    (
                        inference_processed_df,
                        inference_nonprocessed_df,
                        actual_df,
                    ) = await seperate_inference_rows(inference_group)

                    await run_calculate_drifting_metrics_pipeline(
                        model, inference_processed_df, timestamp
                    )

                    await run_calculate_performance_metrics_pipeline(
                        model, inference_processed_df, actual_df, timestamp
                    )

                    await run_calculate_feature_metrics_pipeline(
                        model, inference_processed_df, timestamp
                    )

                    await set_inference_rows_to_used(db, inference_rows_ids)

            logger.info(f"Ended Metrics pipeline for model {model.id}...")

    db.close()
    end = time.time()
    logger.info("Metrics pipeline ended for all models!")
    logger.info("Runtime of Metrics pipeline took {}".format(end - start))
