from sqlalchemy import Column, String, DateTime, JSON, Enum
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship
from whitebox.schemas.model import ModelType


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    name = Column(String)
    description = Column(String)
    type = Column("type", Enum(ModelType))
    labels = Column(JSON, nullable=True)
    prediction = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    dataset_rows = relationship("DatasetRow")
    inference_rows = relationship("InferenceRow")
    binary_classification_metrics = relationship("BinaryClassificationMetrics")
    multi_classification_metrics = relationship("MultiClassificationMetrics")
    regression_metrics = relationship("RegressionMetrics")
    drifting_metrics = relationship("DriftingMetric")
    model_integrity_metrics = relationship("ModelIntegrityMetric")
    model_monitors = relationship("ModelMonitor")
