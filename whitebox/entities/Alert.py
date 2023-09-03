from sqlalchemy import Column, String, ForeignKey, DateTime
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    model_monitor_id = Column(
        String, ForeignKey("model_monitors.id", ondelete="CASCADE")
    )
    timestamp = Column(DateTime(timezone=True))
    description = Column(String)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
