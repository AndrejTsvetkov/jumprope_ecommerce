from app.db import models
from app.db.database import get_engine


def init_db() -> None:
    models.Base.metadata.create_all(bind=get_engine())
