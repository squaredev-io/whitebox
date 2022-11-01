from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class DriftingMetric(Base):
    __tablename__ = "drifting_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    context_distance = Column(Float)
    data_distance = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
