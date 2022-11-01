from typing import Any
from sqlalchemy import Column, Numeric, String, ForeignKey, DateTime
from src.entities.Base import Base
from sqlalchemy.orm import relationship
from src.utils.id_gen import generate_uuid


class ModelMonitor(Base):
    __tablename__ = "model_monitors"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    dataset_id = Column(String, ForeignKey("datasets.id", ondelete="CASCADE"))
    name = Column(String)
    metric = Column(Any) # Define Enum
    threshold = Column(Numeric)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    alerts = relationship("Alert")