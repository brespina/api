from .database import SessionLocal
from typing import Generator

def get_db() -> Generator:
    """
    FastAPI dependency that yields a SQLAlchemy session
    and makes sure it's closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
