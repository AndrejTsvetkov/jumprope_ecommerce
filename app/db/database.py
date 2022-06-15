from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

Base = declarative_base()


def get_engine() -> Engine:
    return create_engine(
        get_settings().SQLALCHEMY_DATABASE_URI,
        connect_args={'check_same_thread': False},
    )


def get_session() -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
