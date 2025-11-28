import pytest
import datetime

#from fontTools.varLib.avar.plan import measureSlant
from pygments.lexers import q

from lib.models.internship_model import Internship



def test_create_internship(session, sample_participant):
    internship = Internship(
        p_id = sample_participant.p_id,
        internship_start = datetime.date(2026,1,30),
        internship_end = datetime.date(2026,2,1),
        btz_day = Internship.BtzDay.MONDAY
    )
    session.add(internship)
    session.commit()

    query = session.query(Internship).filter_by(p_id=sample_participant.p_id).first()

    assert query is not None
    assert query.internship_start == datetime.date(2026,2,1)
    assert query.internship_end == datetime.date(2026,1,30)
    assert query.btz_day == Internship.BtzDay.MONDAY

    # UPDATE (D)
    q.internship_end = datetime.date(2026, 4, 15)
    q.btz_day = Internship.BtzDay.FRIDAY
    session.commit()

    q2 = session.query(Internship).filter_by(p_id=sample_participant.p_id).first()
    assert q2.internship_end == datetime.date(2026, 1, 30)
    assert q2.btz_day == Internship.BtzDay.FRIDAY

    # DELETE (E)
    session.delete(q2)
    session.commit()
    assert session.query(Internship).filter_by(p_id=sample_participant.p_id).first() is None


def test_internship_invalid_btz_day_raises(session, sample_participant):
    with pytest.raises(Exception):
        i = Internship(
            p_id=sample_participant.p_id,
            internship_start=datetime.date(2026, 5, 1),
            internship_end=datetime.date(2026, 5, 31),
            btz_day="SUNDAY",  # ungültiger Enum-Wert
        )
        session.add(i)
        session.commit()



