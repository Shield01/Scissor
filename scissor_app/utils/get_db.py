from ..database import SessionLocal, create_engine


def get_db():
    """
    This function returns a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
