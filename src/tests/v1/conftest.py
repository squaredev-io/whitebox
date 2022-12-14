import databases
import sqlalchemy
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import sessionmaker

from src.core.settings import get_settings
from src.entities.Base import Base
from src.main import app
from src.sdk.whitebox import Whitebox
from src.tests.utils.maps import v1_test_order_map
from secrets import token_hex

settings = get_settings()


def get_order_number(task):
    return v1_test_order_map.index(task)


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
    api_key: str = token_hex(32)
    model_binary: dict = {}
    model_multi: dict = {}
    inference_row_multi: dict = {}
    inference_row_binary: dict = {}


state = TestsState()


class TestsSDKState:
    wb: Whitebox


state_sdk = TestsSDKState()
