# from .Base import Base
from sqlalchemy import Column, String
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import deferred


class User(Base):
    __tablename__ = "users"

    id = Column(String, unique=True, primary_key=True, default=generate_uuid)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = deferred(Column(String))
