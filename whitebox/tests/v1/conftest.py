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
from whitebox.core.db import SessionLocal


settings = get_settings()


def get_order_number(task):
    return v1_test_order_map.index(task)


@fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


class TestsState:
    user: dict = {}
    model_binary: dict = {}
    model_multi: dict = {}
    model_multi_2: dict = {}
    model_multi_3: dict = {}
    model_regression: dict = {}
    inference_row_multi: dict = {}
    inference_row_binary: dict = {}


state = TestsState()


@fixture(scope="session")
def api_key():
    db = SessionLocal()

    user = crud.users.get_first_by_filter(db=db, username="admin")
    api_key = (
        decrypt_api_key(user.api_key, settings.SECRET_KEY.encode())
        if settings.SECRET_KEY
        else user.api_key
    )

    yield api_key


class TestsSDKState:
    wb: Whitebox


state_sdk = TestsSDKState()
