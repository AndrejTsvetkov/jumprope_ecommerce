from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseSettings

basedir = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{basedir / "data.db"}'


@lru_cache()
def get_settings(**kwargs: Any) -> Settings:
    return Settings(**kwargs)
