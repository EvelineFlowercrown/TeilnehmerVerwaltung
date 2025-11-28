# tests/test_vacation_model.py
#from xml.sax.handler import property_interning_dict
import datetime

from lib.models.vacation_model import Vacation


def test_vacation(session, sample_participant):
    # CREATE
    v = Vacation(
        p_id=sample_participant.p_id,
        vacation_start=datetime.date(2023, 1, 1),
        vacation_end=datetime.date(2023, 1, 15),
    )
    session.add(v)
    session.commit()

    q = session.query(Vacation).filter_by(p_id=sample_participant.p_id).first()
    assert q is not None
    assert q.vacation_start == datetime.date(2023, 1, 1)
    assert q.vacation_end == datetime.date(2023, 1, 15)
    assert q.participant == sample_participant

    # UPDATE (D)
    q.vacation_end = datetime.date(2023, 1, 20)
    session.commit()

    q2 = session.query(Vacation).filter_by(p_id=sample_participant.p_id).first()
    assert q2.vacation_end == datetime.date(2023, 1, 20)

    # DELETE (E)
    session.delete(q2)
    session.commit()

    assert (
        session.query(Vacation)
        .filter_by(p_id=sample_participant.p_id,
                   vacation_start=datetime.date(2023, 1, 1))
        .first()
        is None
    )
