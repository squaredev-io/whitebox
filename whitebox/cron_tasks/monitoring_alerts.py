from datetime import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from whitebox import crud, entities
from whitebox.core.settings import get_settings
from whitebox.cron_tasks.shared import (
    get_all_models,
    get_latest_data_drift_metrics_report,
    get_latest_performance_metrics_report,
    get_active_model_monitors,
)
from whitebox.schemas.model import Model, ModelType
from whitebox.schemas.modelMonitor import ModelMonitor, MonitorMetrics
from whitebox.utils.logger import cronLogger as logger

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
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

    if not last_performance_metrics_report:
        logger.info(
            f"No alert created for monitor: {monitor.id} because no performance report was found!"
        )
        return

    if model.type == ModelType.binary or monitor.metric == MonitorMetrics.accuracy:
        metric_value = vars(last_performance_metrics_report)[monitor.metric]
    else:
        metric_value = vars(last_performance_metrics_report)[monitor.metric]["weighted"]

    if metric_value < monitor.lower_threshold:
        new_alert = entities.Alert(
            model_id=model.id,
            model_monitor_id=monitor.id,
            timestamp=str(datetime.utcnow()),
            description=f"{monitor.metric} fell below the threshold of {monitor.lower_threshold} at value {metric_value}.",
        )
        crud.alerts.create(db, obj_in=new_alert)
        logger.info(f"Created alert for monitor {monitor.id}!")


async def run_create_data_drift_alert_pipeline(model: Model, monitor: ModelMonitor):
    """
    Run the pipeline to find any alerts for a metric in performance metrics
    If one is found it is saved in the database
    """

    last_data_drift_report = await get_latest_data_drift_metrics_report(db, model)

    if not last_data_drift_report:
        logger.info(
            f"No alert created for monitor: {monitor.id} because no data drift report was found!"
        )
        return

    data_drift: bool = last_data_drift_report.data_drift_summary["drift_by_columns"][
        monitor.feature
    ]["drift_detected"]

    if data_drift:
        new_alert = entities.Alert(
            model_id=model.id,
            model_monitor_id=monitor.id,
            timestamp=str(datetime.utcnow()),
            description=f'Data drift found in "{monitor.feature}" feature.',
        )
        crud.alerts.create(db, obj_in=new_alert)
        logger.info(f"Created alert for monitor {monitor.id}!")


async def run_create_alerts_pipeline():
    logger.info("Beginning Alerts pipeline for all models!")
    start = time.time()
    engine.connect()

    models = await get_all_models(db)
    if not models:
        logger.info("No models found! Skipping pipeline")
    else:
        for model in models:
            model_monitors = await get_active_model_monitors(db, model_id=model.id)
            for monitor in model_monitors:
                if (
                    monitor.metric
                    in [
                        MonitorMetrics.accuracy,
                        MonitorMetrics.precision,
                        MonitorMetrics.recall,
                        MonitorMetrics.f1,
                    ]
                    and model.type is not ModelType.regression
                ):
                    await run_create_performance_metric_alert_pipeline(model, monitor)
                elif monitor.metric == MonitorMetrics.data_drift:
                    await run_create_data_drift_alert_pipeline(model, monitor)

    db.close()
    end = time.time()
    logger.info("Alerts pipeline ended for all models!")
    logger.info("Runtime of Alerts pipeline took {}".format(end - start))
