import pytest
import datetime

from fontTools.varLib.avar.plan import measureSlant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models.participant_model import Participant  # Importpfad
from lib.database import BaseClass


@pytest.fixture
def session():
    """Setup für eine In-Memory SQLite DB und Session."""
    engine = create_engine("sqlite:///:memory:")
    BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_participant(session):
    participant = Participant(
        surname="Mustermann",
        first_name="Max",
        btz_start=datetime.date(2023, 1, 1),
        btz_end=datetime.date(2023, 12, 31),
        pt_id=1,
        ps_id=2,
        gdb=True,
        bvb=False,
        seat=7,
        initials="MM",
        table=3,
        measure="KIM",
    )
    session.add(participant)
    session.commit()

    query = session.query(Participant).filter_by(surname="Mustermann").first()

    assert query is not None
    assert query.first_name == "Max"
    assert query.seat == 7
    assert query.initials == "MM"
    assert query.btz_start == datetime.date(2023, 1, 1)
    assert query.gdb is True
    assert query.bvb is False
