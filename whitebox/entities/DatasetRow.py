from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class DatasetRow(Base):
    __tablename__ = "dataset_rows"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    nonprocessed = Column(JSON)
    processed = Column(JSON)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
