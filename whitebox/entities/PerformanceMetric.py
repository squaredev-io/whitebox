from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, JSON
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class BinaryClassificationMetrics(Base):
    __tablename__ = "binary_classification_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1 = Column(Float)
    true_negative = Column(Integer)
    false_positive = Column(Integer)
    false_negative = Column(Integer)
    true_positive = Column(Integer)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))


class MultiClassificationMetrics(Base):
    __tablename__ = "multi_classification_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True))
    accuracy = Column(Float)
    precision = Column(JSON)
    recall = Column(JSON)
    f1 = Column(JSON)
    confusion_matrix = Column(JSON)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))


class RegressionMetrics(Base):
    __tablename__ = "regression_metrics"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True))
    r_square = Column(Float)
    mean_squared_error = Column(Float)
    mean_absolute_error = Column(Float)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
