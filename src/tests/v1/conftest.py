from pytest import fixture
from fastapi.testclient import TestClient
from src.main import app
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from src.models.Base import Base
from src.core.settings import get_settings


settings = get_settings()
test_order_map = {
    "seed_data": 0,
    "seed_data_drop": 1999999,
    "health": 1,
    "auth": {"unauthorized_me": 2, "login": 3, "authorized_me": 4},
    "users": {"create": 5, "get_all": 6, "get": 7, "update": 8, "delete": 102},
    "projects": {"create": 9, "get_all": 13, "get": 14, "update": 15, "delete": 101},
    "models": {"create": 17, "get_all": 18, "get": 19, "update": 20, "delete": 100},
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
    client: dict = {}
    project: dict = {}


state = TestsState()
