from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = ""
    ENV: str = ""
    SECRET_KEY: str = ""
    ACCESS_TOKEN_LIFE_IN_HOURS: str = ""
    ALGORITHM: str = ""
    NEO4J_URI: str = ""
    NEO4J_USER: str = ""
    NEO4J_PASS: str = ""
    POSTGRES_DB_URI: str = ""
    POSTGRES_JDBC_URI: str = ""
    VERSION: str = ""

    class Config:
        env_file = f".env.{os.getenv('ENV')}" or ".env.dev"


@lru_cache()
def get_settings():
    return Settings()


class SimulatorSettings(Settings):
    APP_NAME_SIMULATOR: str

    class Config:
        env_file = f".env.{os.getenv('ENV')}" or ".env.dev"


@lru_cache()
def get_simulator_settings():
    return SimulatorSettings()


class CronSettings(Settings):
    APP_NAME_CRON: str
    API_KEY: str

    class Config:
        env_file = f".env.{os.getenv('ENV')}" or ".env.dev"


@lru_cache()
def get_cron_settings():
    return CronSettings()
