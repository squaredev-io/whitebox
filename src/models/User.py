# from .Base import Base
from sqlalchemy import Column, String, ForeignKey, ARRAY
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, unique=True, primary_key=True, default=generate_uuid)
    ext_id = Column(String, unique=True, primary_key=True)
    name = Column(String)
    app = relationship("App", back_populates="users")
    app_id = Column(String, ForeignKey("apps.id", ondelete="CASCADE"))
