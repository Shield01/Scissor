from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env_name: str = ""
    base_url: str = ""
    db_url: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = ""

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    This function returns an instance of the Settings class and prints a message indicating which
    environment's settings are being loaded.
    :return: an instance of the `Settings` class.
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
