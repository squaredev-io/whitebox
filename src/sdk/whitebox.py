from typing import Dict, Optional

import requests
from src.schemas.model import FeatureTypes, ModelCreateDto, ModelType
import logging

logger = logging.getLogger(__name__)


class Whitebox:
    def __init__(self, host: str, api_key: str, verbose: bool = False):
        self.host = host
        self.api_key = api_key
        self.verbose = verbose

    def create_model(
        self,
        name: str,
        type: ModelType,
        features: Dict[str, FeatureTypes],
        prediction: str,
        probability: str,
        labels: Optional[Dict[str, int]],
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
            url=f"{self.host}/v1/models",
            json=new_model.dict(),
            headers={"api-key": self.api_key},
        )

        logger.info(result.json())
        return result.json()

    def get_model(self):
        pass

    def delete_model(self):
        pass

    def log_training_dataset(self):
        pass

    def log_inference(self):
        pass

    def log_actual(self):
        pass
