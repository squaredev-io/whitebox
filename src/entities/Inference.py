from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class Inference(Base):
    __tablename__ = "inferences"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime)
    features = Column(JSON)
    raw = Column(JSON)
    prediction = Column(JSON)
    actuals = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
