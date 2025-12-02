import pytest

from lib.models.ps_staff_model import PsStaff


def test_create_ps_staff(session, sample_ps):
    ps = PsStaff(first_name="Marie", surname="Lue")
    session.add(ps)
    session.commit()

    q = session.query(PsStaff).filter_by(ps_id=ps.ps_id).first()
    assert q is not None
    assert q.first_name == "Marie"
    assert q.surname == "Lue"
