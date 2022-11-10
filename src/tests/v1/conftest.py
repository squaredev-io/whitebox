from pytest import fixture
from fastapi.testclient import TestClient
from src.main import app
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from src.entities.Base import Base
from src.core.settings import get_settings


settings = get_settings()
test_order_map = {
    "seed_data": 0,
    "seed_data_drop": 1999999,
    "health": 1,
    "auth": {"unauthorized_me": 2, "login": 3, "authorized_me": 4},
    "users": {"create": 5, "get_all": 6, "get": 7, "update": 8, "delete": 102},
    "models": {"create": 9, "get_all": 10, "get": 11, "update": 12, "delete": 100},
    "inference_rows": {"create": 13, "create_many": 14, "get_model's_all": 15, "get": 16},
    "performance_metrics": {"get_model's_all": 17},
    "drifting_metrics": {"get_model's_all": 18, "get": 19},
    "model_integrity_metrics": {"get_model's_all": 20, "get": 21},
    "dataset_rows": {"create": 25, "get_model's_all": 26, "create_model_doesn't_exist": 27},
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


class TestsState:
    user: dict = {}
    model: dict = {}
    inference_row: dict = {}


state = TestsState()
