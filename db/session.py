"""Create data base session."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def session():
    """Create database session."""
    engine = create_engine('sqlite:////opt/server/server.db', echo=True)
    new_session = sessionmaker(bind=engine)
    return new_session()
