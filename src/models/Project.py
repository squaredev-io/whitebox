from sqlalchemy import Column, String, ForeignKey, DateTime
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # models = relationship("Model")
