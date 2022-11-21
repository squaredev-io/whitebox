from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Enum
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship
from src.schemas.model import ModelType


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    name = Column(String)
    description = Column(String)
    type = Column("type", Enum(ModelType))
    features = Column(JSON)
    labels = Column(JSON, nullable=True)
    prediction = Column(String)
    probability = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    dataset_rows = relationship("DatasetRow")
    inference_rows = relationship("InferenceRow")
    binary_classification_metrics = relationship("BinaryClassificationMetrics")
    multi_classification_metrics = relationship("MultiClassificationMetrics")
    drifting_metrics = relationship("DriftingMetric")
    model_integrity_metrics = relationship("ModelIntegrityMetric")
    model_monitors = relationship("ModelMonitor")
