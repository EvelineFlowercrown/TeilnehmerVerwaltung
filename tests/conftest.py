import smtplib

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.database import BaseClass

@pytest.fixture(scope="function")
def session():
    """Setup für eine In-Memory SQLite DB und Session."""
    engine = create_engine("sqlite:///:memory:")
    BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()