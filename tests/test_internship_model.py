import pytest
import datetime

from fontTools.varLib.avar.plan import measureSlant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models.internship_model import Internship
from lib.database import BaseClass


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    BaseClass.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_internship(session):
    internship = Internship(
        p_id = 123, 
        internship_start=datetime.date(2026,2,1),
        internship_end=datetime.date(2026,1,30),
        btz_day=Internship.BtzDay.MONDAY
    )
    session.add(internship)
    session.commit()

    query = session.query(Internship).filter_by(p_id=123).first()

    assert query is not None
    assert query.internship_start == datetime.date(2026,2,1)
    assert query.internship_end == datetime.date(2026,1,30)
    assert query.btz_day == Internship.BtzDay.MONDAY


