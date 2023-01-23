import databases
import sqlalchemy
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import sessionmaker
from whitebox import crud

from whitebox.core.settings import get_settings
from whitebox.entities.Base import Base
from whitebox.main import app
from whitebox.sdk.whitebox import Whitebox
from whitebox.tests.utils.maps import v1_test_order_map
from whitebox.entities.Base import Base
from whitebox.utils.passwords import decrypt_api_key


settings = get_settings()

database = databases.Database(settings.DATABASE_URL)
engine = sqlalchemy.create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_order_number(task):
    return v1_test_order_map.index(task)


@fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


class TestsState:
    user: dict = {}
    api_key: str = ""
    model_binary: dict = {}
    model_multi: dict = {}
    model_multi_2: dict = {}
    model_multi_3: dict = {}
    inference_row_multi: dict = {}
    inference_row_binary: dict = {}


state = TestsState()


@fixture(scope="session", autouse=True)
def get_admin_token():
    Base.metadata.create_all(engine)
    db = SessionLocal()

    user = crud.users.get_first_by_filter(db=db, username="admin")
    state.api_key = (
        decrypt_api_key(user.api_key, settings.SECRET_KEY.encode())
        if settings.SECRET_KEY
        else user.api_key
    )

    db.close()


class TestsSDKState:
    wb: Whitebox


state_sdk = TestsSDKState()
