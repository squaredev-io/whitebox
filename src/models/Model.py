# from .Base import Base
from sqlalchemy import Column, String, Boolean
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship
from sqlalchemy.orm import deferred


class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = deferred(Column(String))
    verified = Column(Boolean, default=False)
    apps = relationship("App", back_populates="client")
