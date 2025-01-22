from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    TRAINING_BOT_TOKEN: str
    OPENWEATHERMAP_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_config():
    return Config()