# from .Base import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Enum
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String)
    type = Column(Enum) # Define Enum
    features =  Column(JSON)
    predictions = Column(JSON)
    labels = Column(String)
    feature_importance = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
