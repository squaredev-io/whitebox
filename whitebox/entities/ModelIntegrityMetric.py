from sqlalchemy import Column, JSON, Float, ForeignKey, String, DateTime
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class ModelIntegrityMetric(Base):
    __tablename__ = "model_integrity_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True))
    feature_metrics = Column(JSON)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
