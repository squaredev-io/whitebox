from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class DatasetRow(Base):
    __tablename__ = "dataset_rows"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    dataset_id = Column(String, ForeignKey("datasets.id", ondelete="CASCADE"))
    nonprocessed = Column(JSON)
    processed = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
