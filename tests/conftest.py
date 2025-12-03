import pytest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.database import BaseClass
from lib.models import PsStaff, PtStaff
from lib.models.participant_model import Participant


@pytest.fixture(scope="session")
def engine():
    """
    Create an in-memory SQLite database and initialize all tables once for the
    entire test session.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    BaseClass.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def session(engine):
    """
    Open a database connection, start a transaction for the test, and roll back
    all changes afterwards.
    """
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def sample_ps(session):
    """
    Create sample PsStaff object and add it to the test db session.
    """
    ps = PsStaff(first_name="Anna", surname="Sachbearbeiter")
    session.add(ps)
    session.commit()
    return ps


@pytest.fixture(scope="function")
def sample_pt(session):
    """
    Create sample PtStaff object and add it to the test db session.
    """
    pt = PtStaff(first_name="Peter", surname="Trainer")
    session.add(pt)
    session.commit()
    return pt


@pytest.fixture(scope="function")
def sample_participant(session, sample_ps, sample_pt):
    """
    Create sample Participant object and add it to the test db session.
    """
    p = Participant(
        surname="Tester",
        first_name="Max",
        btz_start=datetime.date(2024, 1, 1),
        btz_end=datetime.date(2024, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_ps.ps_id,
        pt_id=sample_pt.pt_id,
    )
    session.add(p)
    session.commit()
    return p
