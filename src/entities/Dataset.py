from sqlalchemy import Column, String, ForeignKey, DateTime
from src.entities.Base import Base
from sqlalchemy.orm import relationship
from src.utils.id_gen import generate_uuid


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String)
    target = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    model_monitors = relationship("ModelMonitor")
    dataset_rows = relationship("DatasetRow")
