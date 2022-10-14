# from .Base import Base
from sqlalchemy import Column, String, ForeignKey
from src.models.Base import Base
from src.utils.id_gen import generate_uuid
from sqlalchemy.orm import relationship


# class App(Base):
#     __tablename__ = "apps"

#     id = Column(String, unique=True, primary_key=True, default=generate_uuid)
#     name = Column(String)
#     secret = Column(String)
#     client_id = Column(String, ForeignKey("clients.id", ondelete="CASCADE"))
#     client = relationship("Client", back_populates="apps")
#     catalog_id = Column(String, ForeignKey("catalogs.id"))
#     users = relationship("User", back_populates="app")
