import smtplib

import pytest

@pytest.fixture(scope="session")
def session():
    """Setup für eine In-Memory SQLite DB und Session."""
    engine = create_engine("sqlite:///:memory:")
    BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()