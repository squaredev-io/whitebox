from src.analytics.drift.pipelines import (
    create_data_drift_pipeline,
    create_concept_drift_pipeline,
)
from src.core.settings import get_settings
from src.crud.drifting_metrics import drifting_metrics
from src.core.db import SessionLocal, get_db
from src.cron_tasks.shared import (
    get_model_inference_rows_df,
    get_all_models,
    get_model_dataset_rows_df,
)
from src.entities.DriftingMetric import DriftingMetric
from datetime import datetime

settings = get_settings()
db = SessionLocal()


async def run_create_data_drift_pipeline():
    models = await get_all_models(db)

    for model in models:
        inference_df = await get_model_inference_rows_df(db, model_id=model.id)
        training_df = await get_model_dataset_rows_df(db, model_id=model.id)

        data_drif_report = create_data_drift_pipeline(training_df, inference_df)
        # concept_drift_report = create_concept_drift_pipeline(
        #     training_df, inference_df, "fw"
        # )

        new_drifting_metric = DriftingMetric(
            timestamp=str(datetime.utcnow()),
            model_id=model.id,
            concept_drift_summary=data_drif_report,
            data_drift_summary=data_drif_report,
        )

        drifting_metrics.create(db, obj_in=new_drifting_metric)
