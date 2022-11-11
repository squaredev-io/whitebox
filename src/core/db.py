from src.core.settings import get_settings
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from src.entities.Base import Base

settings = get_settings()
database = databases.Database(settings.POSTGRES_DB_URI)
engine = sqlalchemy.create_engine(settings.POSTGRES_DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def connect():
    """
    Connect to DB
    """
    Base.metadata.create_all(engine)
    await database.connect()


async def close():
    """
    Close DB Connection
    """
    await database.disconnect()
    # logging.info("Closed connection with DB")
