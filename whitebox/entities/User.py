from sqlalchemy import Column, String, DateTime
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid
from sqlalchemy.orm import deferred, relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, unique=True, primary_key=True, default=generate_uuid)
    username = Column(String)
    api_key = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
