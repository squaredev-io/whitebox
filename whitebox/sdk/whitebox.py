from enum import Enum
import numpy as np
import pandas as pd
from whitebox.schemas.model import FeatureTypes, ModelCreateDto, ModelType
from typing import Dict, Optional
import requests
import logging
from fastapi import status

from whitebox.schemas.modelMonitor import (
    AlertSeverity,
    ModelMonitorCreateDto,
    MonitorMetrics,
    MonitorStatus,
)


class APiVersion(str, Enum):
    v1 = "v1"


logger = logging.getLogger(__name__)


class Whitebox:
    def __init__(
        self,
        host: str,
        api_key: str,
        verbose: bool = False,
        api_version: APiVersion = APiVersion.v1,
    ):
        self.host = host
        self.api_key = api_key
        self.verbose = verbose
        self.api_version = api_version

    def create_model(
        self,
        name: str,
        type: ModelType,
        features: Dict[str, FeatureTypes],
        prediction: str,
        probability: str,
        labels: Dict[str, int],
        description: str = "",
    ):
        """
        Create a new model in Whitebox and define a type, and a schema for it.
        """
        new_model = ModelCreateDto(
            name=name,
            description=description,
            type=type,
            features=features,
            labels=labels,
            prediction=prediction,
            probability=probability,
        )
        result = requests.post(
            url=f"{self.host}/{self.api_version}/models",
            json=new_model.dict(),
            headers={"api-key": self.api_key},
        )

        logger.info(result.json())
        return result.json()

    def get_model(self, model_id: str):
        """
        Returns a model by its id. If the model does not exist, returns None.
        """
        result = requests.get(
            url=f"{self.host}/{self.api_version}/models/{model_id}",
            headers={"api-key": self.api_key},
        )
        if result.status_code == status.HTTP_404_NOT_FOUND:
            return None

        return result.json()

    def delete_model(self, model_id: str):
        """
        Deletes a model by its id. If any error occurs, returns False.
        """
        result = requests.delete(
            url=f"{self.host}/{self.api_version}/models/{model_id}",
            headers={"api-key": self.api_key},
        )

        if result.status_code == status.HTTP_200_OK:
            return True

        return False

    def log_training_dataset(
        self, model_id: str, non_processed: pd.DataFrame, processed: pd.DataFrame
    ) -> bool:
        """
        Logs a training dataset for a model.

        Non processed is a dataframe with the raw data.
        Processed is a dataframe with the data after it has been processed and before it has entered the model.
        """
        self._check_processed_and_non_processed_length(processed, non_processed)
        non_processed_json = non_processed.to_dict(orient="records")
        processed_json = processed.to_dict(orient="records")

        dataset_rows = []
        for i in range(len(non_processed)):
            dataset_rows.append(
                dict(
                    model_id=model_id,
                    nonprocessed=non_processed_json[i],
                    processed=processed_json[i],
                )
            )

        result = requests.post(
            url=f"{self.host}/{self.api_version}/dataset-rows",
            headers={"api-key": self.api_key},
            json=dataset_rows,
        )
        if result.status_code == status.HTTP_201_CREATED:
            return True

        return False

    def log_inferences(
        self,
        model_id: str,
        non_processed: pd.DataFrame,
        processed: pd.DataFrame,
        timestamps: pd.Series,
        actuals: pd.Series = None,
    ) -> bool:
        """
        Logs inferences of a model.

        Non processed is a dataframe with the raw data.
        Processed is a dataframe with the data after it has been processed and before it has entered the model.
        """
        self._check_processed_and_non_processed_length(processed, non_processed)
        non_processed_json = non_processed.to_dict(orient="records")
        processed_json = processed.to_dict(orient="records")
        timestamps_list = timestamps.tolist()

        if actuals is not None:
            actuals = actuals.replace({np.nan: None})
            actuals_list = actuals.tolist()
        else:
            actuals_list = actuals

        inference_rows = []
        for i in range(len(non_processed)):
            inference_rows.append(
                dict(
                    model_id=model_id,
                    nonprocessed=non_processed_json[i],
                    processed=processed_json[i],
                    timestamp=timestamps_list[i],
                    actual=actuals_list[i] if actuals_list is not None else None,
                )
            )

        result = requests.post(
            url=f"{self.host}/{self.api_version}/inference-rows/batch",
            headers={"api-key": self.api_key},
            json=inference_rows,
        )
        if result.status_code == status.HTTP_201_CREATED:
            return True

        return False

    def _check_processed_and_non_processed_length(
        self, processed: pd.DataFrame, non_processed: pd.DataFrame
    ) -> bool:
        """
        Checks if the processed and non processed dataframes have the same number of rows.
        """
        if len(processed) != len(non_processed):
            raise ValueError(
                "Processed and non processed dataframes must have the same length."
            )
        return True

    def create_model_monitor(
        self,
        model_id: str,
        name: str,
        status: MonitorStatus,
        metric: MonitorMetrics,
        feature: Optional[str],
        lower_threshold: Optional[float],
        severity: AlertSeverity,
        email: str,
    ) -> dict:
        """
        Creates a monitor for a model.
        """

        model_monitor = ModelMonitorCreateDto(
            model_id=model_id,
            name=name,
            status=status,
            metric=metric,
            feature=feature,
            lower_threshold=lower_threshold,
            severity=severity,
            email=email,
        )

        result = requests.post(
            url=f"{self.host}/{self.api_version}/model-monitors",
            json=model_monitor.dict(),
            headers={"api-key": self.api_key},
        )

        logger.info(result.json())
        return result.json()

    def get_alerts(self, model_id: str) -> dict:
        """
        Returns all alerts for a model.
        """
        result = requests.get(
            url=f"{self.host}/{self.api_version}/alerts?modelId={model_id}",
            headers={"api-key": self.api_key},
        )

        logger.info(result.json())
        return result.json()
