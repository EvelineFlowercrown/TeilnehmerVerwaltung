from xml.sax.handler import property_interning_dict

import pytest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.vacation_model import Vacation
from lib.models.participant_model import Participant
import lib.database

@pytest.fixture
def session():
    """Setup für eine In-Memory SQLite DB und Session."""
    engine = create_engine('sqlite:///:memory:')
    lib.database.BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_vacation(session):
    vacation = Vacation(
        p_id = Participant.p_id,
        vacation_start = datetime.date(2023, 1, 1),
        vacation_end =datetime.date(2023, 1, 31)
    )
    session.add(vacation)
    session.commit()

    query = session.query(vacation).filter_by(p_id= Participant.p_id ).first()

    assert query is not None
    assert query.p_id == Participant.p_id
    assert query.vacation_start == datetime.date(2023, 1, 1)
    assert query.vacation_en == datetime.date(2023, 1, 31)

