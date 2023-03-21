from typing import List, Union
from whitebox.middleware.auth import authenticate_user
from whitebox.schemas.modelMonitor import (
    ModelMonitor,
    ModelMonitorCreateDto,
    ModelMonitorUpdateDto,
    MonitorMetrics,
)
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.schemas.user import User
from whitebox.schemas.utils import StatusCode
from whitebox.utils.errors import add_error_responses, errors


model_monitors_router = APIRouter()


@model_monitors_router.post(
    "/model-monitors",
    tags=["Model Monitors"],
    response_model=ModelMonitor,
    summary="Create a model monitor",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 401, 409]),
)
async def create_model_monitor(
    body: ModelMonitorCreateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> ModelMonitor:
    """Inserts a model monitor into the database."""

    model = crud.models.get(db, body.model_id)
    if not model:
        return errors.not_found("Model not found!")

    if body.metric in [MonitorMetrics.concept_drift, MonitorMetrics.data_drift]:
        if body.metric == MonitorMetrics.concept_drift:
            body.feature = model.target_column
        else:
            if not body.feature:
                return errors.bad_request(f"Please set a feature for the monitor!")
            # TODO This should get the feature columns from model.features when this field is
            # automatically updated from the training dataset.
            dataset_row = crud.dataset_rows.get_first_by_filter(db, model_id=model.id)
            if not dataset_row:
                return errors.not_found(
                    f"No training dataset found for model: {model.id}!\
                    Insert the taining dataset and then create a monitor!"
                )
            features = dataset_row.processed
            if body.feature not in features:
                return errors.bad_request(
                    f"Monitored featured must be in the dataset's features!"
                )
            if body.feature == model.target_column:
                return errors.bad_request(
                    f"Monitored featured cannot be the target column in data drift!"
                )
        body.lower_threshold = None
    else:
        if body.lower_threshold is None:
            return errors.bad_request(f"Please set a lower threshold for the monitor!")
        body.feature = None

    new_model_monitor = crud.model_monitors.create(db=db, obj_in=body)
    return new_model_monitor


@model_monitors_router.get(
    "/model-monitors",
    tags=["Model Monitors"],
    response_model=List[ModelMonitor],
    summary="Get all model's model monitors",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def get_all_models_model_monitors(
    model_id: Union[str, None] = None,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
):
    """
    Fetches model monitors from the databse.
    \n If a model id is provided, only the monitors for the specific model will be fetched.
    \n If a model id is not provided then all monitors from the database will be fetched.
    """

    if model_id:
        model = crud.models.get(db, model_id)
        if model:
            return crud.model_monitors.get_model_monitors_by_model(
                db=db, model_id=model_id
            )
        else:
            return errors.not_found("Model not found")
    else:
        return crud.model_monitors.get_all(db=db)


@model_monitors_router.put(
    "/model-monitors/{model_monitor_id}",
    tags=["Model Monitors"],
    response_model=ModelMonitor,
    summary="Update model monitor",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([400, 401, 404]),
)
async def update_model_monitor(
    model_monitor_id: str,
    body: ModelMonitorUpdateDto,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> ModelMonitor:
    """Updates record of the model monitor with the specified id."""

    # Remove all unset properties (with None values) from the update object
    filtered_body = {k: v for k, v in dict(body).items() if v is not None}

    model_monitor = crud.model_monitors.get(db=db, _id=model_monitor_id)

    if not model_monitor:
        return errors.not_found("Model monitor not found!")

    if model_monitor.metric in [
        MonitorMetrics.concept_drift,
        MonitorMetrics.data_drift,
    ]:
        filtered_body["lower_threshold"] = None

    return crud.model_monitors.update(db=db, db_obj=model_monitor, obj_in=filtered_body)


@model_monitors_router.delete(
    "/model-monitors/{model_monitor_id}",
    tags=["Model Monitors"],
    response_model=StatusCode,
    summary="Delete model monitor",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([401, 404]),
)
async def delete_model_monitor(
    model_monitor_id: str,
    db: Session = Depends(get_db),
    authenticated_user: User = Depends(authenticate_user),
) -> StatusCode:
    """Deletes the model monitor with the specified id from the database."""

    model_monitor = crud.model_monitors.get(db=db, _id=model_monitor_id)
    if not model_monitor:
        return errors.not_found("Model monitor not found")

    crud.model_monitors.remove(db=db, _id=model_monitor_id)
    return {"status_code": status.HTTP_200_OK}
