from sqlalchemy import Column, JSON, Float, ForeignKey, String, DateTime
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class ModelIntegrityMetric(Base):
    __tablename__ = "model_integrity_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    missing_values = Column(Float)
    feature_metrics = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
