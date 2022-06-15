from typing import Generator

from sqlalchemy.orm import Session

from app.db.database import get_session


def get_db() -> Generator[Session, None, None]:
    session_local = get_session()
    db = session_local()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
