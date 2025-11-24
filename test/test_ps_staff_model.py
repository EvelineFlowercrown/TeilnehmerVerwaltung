import pytest

from fontTools.varLib.avar.plan import measureSlant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models.participant_model import Participant
from lib.database import BaseClass

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_ps_staff(session):
    ps_staff = PsStaff(
        ps_id = 456,
        first_name_ps = "Karl",
        surname_ps = "Marx",
    )
    session.add(ps_staff)
    session.commit()

    query = session.query(PsStaff).filter_by(surname_ps="Marx").first()

    assert query is not None
    assert query.ps_id == 456
    assert query.first_name_ps == "Karl"
    assert query.surname_ps == "Marx"
