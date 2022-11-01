from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    precision = Column(Float)
    recall = Column(Float)
    f1 = Column(Float)
    accuracy = Column(Float)
    true_positives= Column(Integer)
    true_negatives= Column(Integer)
    false_positives= Column(Integer)
    false_negatives= Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
