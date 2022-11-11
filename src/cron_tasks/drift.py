from src.analytics.drift.pipelines import create_data_drift_pipeline, create_concept_drift_pipeline
from src.core.settings import get_settings
from src.crud.drifting_metrics import drifting_metrics
from src.core.db import get_db
from src.cron_tasks.shared import get_model_inference_rows_df, get_all_models, get_model_dataset_rows_df
from src.schemas.driftingMetric import DriftingMetricBase
from datetime import datetime

settings = get_settings()
db = get_db()

async def run_create_data_drift_pipeline():

  models = await get_all_models(db)

  for model in models:
    inference_df = await get_model_inference_rows_df(db, model_id=model.id)
    training_df = await get_model_dataset_rows_df(db, model_id=model.id)
  
    data_drif_report = create_data_drift_pipeline(training_df, inference_df)
    concept_drift_report = create_concept_drift_pipeline(training_df, inference_df)


    new_drifting_metric = DriftingMetricBase(
      timestamp=datetime.utcnow(),
      model_id=model.id,
      concept_drift_summary=concept_drift_report,
      data_drift_summary=data_drif_report
    )

    print(new_drifting_metric)
    drifting_metrics.create(db, new_drifting_metric)


