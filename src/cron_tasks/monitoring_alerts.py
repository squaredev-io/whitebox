from datetime import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src import crud, entities
from src.core.settings import get_settings
from src.cron_tasks.shared import (
    get_all_models,
    get_latest_performance_metrics_report,
    get_model_monitors,
)
from src.schemas.model import Model, ModelType
from src.schemas.modelMonitor import ModelMonitor, MonitorMetrics
from src.utils.logger import cronLogger as logger

settings = get_settings()

engine = create_engine(settings.POSTGRES_DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


async def run_create_performance_metric_alert_pipeline(
    model: Model, monitor: ModelMonitor
):
    """
    Run the pipeline to find any alerts for a metric in performance metrics
    If one is found it is saved in the database
    """

    last_performance_metrics_report = await get_latest_performance_metrics_report(
        db, model
    )

    if model.type == ModelType.binary or monitor.metric == MonitorMetrics.accuracy:
        metric_value = last_performance_metrics_report[monitor.metric]
    else:
        metric_value = last_performance_metrics_report[monitor.metric]["weighted"]

    if metric_value < monitor.threshold:
        new_alert = entities.Alert(
            model_id=model.id,
            model_monitor_id=monitor.id,
            timestamp=str(datetime.utcnow()),
            description=f"{monitor.metric} fell below the threshold of {monitor.threshold} at value {metric_value}.",
        )
        crud.alerts.create(db, obj_in=new_alert)
        logger.info(f"Created alert for monitor {monitor.id}!")


async def run_create_alerts_pipeline():
    """
    Run the pipeline to calculate the feature metrics
    After the metrics are calculated they are saved in the database
    """
    models = await get_all_models(db)
    if not models:
        logger.info("No models found! Skipping pipeline")
    else:
        for model in models:
            model_monitors = await get_model_monitors(db, model_id=model.id)
            for monitor in model_monitors:
                if monitor.metric in [
                    MonitorMetrics.accuracy,
                    MonitorMetrics.precision,
                    MonitorMetrics.recall,
                    MonitorMetrics.f1,
                ]:
                    await run_create_performance_metric_alert_pipeline(model, monitor)

    logger.info(f"Calculating feature metrics for model {model.id}")
