from sqlalchemy import Column, ForeignKey, String, DateTime, JSON
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class DriftingMetric(Base):
    __tablename__ = "drifting_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime)
    concept_drift_summary = Column(JSON)
    data_drift_summary = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
