import pytest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from lib.database import BaseClass
from lib.models import PsStaff, PtStaff
from lib.models.participant_model import Participant

# WICHTIG: alle Models müssen irgendwo importiert sein,
# damit sie in BaseClass.metadata registriert sind.


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
def session():
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
        transaction.rollback()
        connection.close()
        clear_mappers()


@pytest.fixture(scope="function")
def sample_staff(session):
    """
    Legt je einen PsStaff und PtStaff an, für Participant & Co.
    """
    ps = PsStaff(first_name_ps="Anna", surname_ps="Sachbearbeiter")
    pt = PtStaff(first_name_pt="Peter", surname_pt="Trainer")
    session.add_all([ps, pt])
    session.commit()
    return {"ps": ps, "pt": pt}


@pytest.fixture(scope="function")
def sample_participant(session, sample_staff):
    """
    Minimaler Participant für Vacation, Internship, KitchenDuty-Relationen etc.
    """
    p = Participant(
        surname="Tester",
        first_name="Max",
        btz_start=datetime.date(2024, 1, 1),
        btz_end=datetime.date(2024, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )
    session.add(p)
    session.commit()
    return p


@pytest.fixture(scope="function")
def sample_kitchen_duty(session):
    """
    Ein einfaches KitchenDuty-Objekt.
    """
    kd = KitchenDuty(
        kd_start=datetime.date(2024, 1, 1),
        kd_end=datetime.date(2024, 1, 5),
    )
    session.add(kd)
    session.commit()
    return kd
