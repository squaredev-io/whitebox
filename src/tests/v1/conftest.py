from pytest import fixture
from fastapi.testclient import TestClient
from src.main import app
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from src.models.Base import Base
from src.core.settings import get_settings
# from src.simulator import simulator_app
# from src.cron import cron_app

settings = get_settings()
test_order_map = {
    "seed_data": 0,
    "seed_data_drop": 1999999,
    "health": 1,
    "auth": {"unauthorized_me": 2, "login": 3, "authorized_me": 4},
    "client": {"register": 5, "update": 6, "delete": 7},
    "users": {"create": 8, "get_all": 9, "get": 10, "update": 11, "delete": 12},
}


@fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@fixture(scope="session", autouse=True)
async def db():

    # runs once before all tests
    engine = sqlalchemy.create_engine(settings.POSTGRES_DB_URI)
    database = databases.Database(settings.POSTGRES_DB_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    await database.connect()
    db = SessionLocal()
    yield db
    # runs once after all tests
    await database.disconnect()
    # await database.execute(query="DROP DATABASE test WITH (FORCE);")
    Base.metadata.drop_all(engine)


# @fixture(scope="session")
# def simulator_client():
#     with TestClient(simulator_app) as simulator_client:
#         yield simulator_client


# @fixture(scope="session")
# def cron_client():
#     with TestClient(cron_app) as cron_client:
#         yield cron_client


class DataHolder:
    client = None
