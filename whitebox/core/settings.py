from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = ""
    ENV: str = ""
    DATABASE_URL: str = ""
    VERSION: str = ""
    MODEL_PATH: str = ""

    class Config:
        env_file = f".env.{os.getenv('ENV')}" or ".env.dev"


@lru_cache()
def get_settings():
    return Settings()


class CronSettings(Settings):
    APP_NAME_CRON: str
    METRICS_CRON: str

    class Config:
        env_file = f".env.{os.getenv('ENV')}" or ".env.dev"


@lru_cache()
def get_cron_settings():
    return CronSettings()
