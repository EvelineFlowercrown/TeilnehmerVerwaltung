# from xml.sax.handler import property_interning_dict
import datetime
import pytest

from lib.models.vacation_model import Vacation


#region: Vacation Factory Fixtures
@pytest.fixture(scope="function")
def vacation_factory(sample_participant):
    """
    Factory fixture to create Vacation object with customizable dates.
    """
    def _factory(
        start=datetime.date(2026, 1, 1),
        end=datetime.date(2026, 1, 15)
    ):
        return Vacation(
            p_id=sample_participant.p_id,
            vacation_start=start,
            vacation_end=end
        )
    return _factory


@pytest.fixture(scope="function")
def sample_vacation(session, vacation_factory):
    """
    Convenience fixture providing a default Vacation object using 
    vacation_factory. Adds to sessions and commits.
    """
    v = vacation_factory()
    session.add(v)
    session.commit()
    return v
#endregion: Vacation Factory Fixtures


#region: CRUD-Tests
def test_create_vacation(session, vacation_factory, sample_participant):
    v = vacation_factory(
        start=datetime.date(2023, 1, 1), 
        end=datetime.date(2023, 1, 15),
        )
    session.add(v)
    session.commit()

    q = session.query(Vacation).filter_by(p_id=sample_participant.p_id).first()
    assert q is not None
    assert q.vacation_start == datetime.date(2023, 1, 1)
    assert q.vacation_end == datetime.date(2023, 1, 15)
    assert q.participant == sample_participant


def test_read_vacation(sample_vacation, sample_participant):
    assert sample_vacation is not None
    assert sample_vacation.vacation_start == datetime.date(2026, 1, 1)
    assert sample_vacation.vacation_end == datetime.date(2026, 1, 15)
    assert sample_vacation.participant == sample_participant


def test_update_vacation(session, vacation_factory, sample_participant):
    v = vacation_factory(end=datetime.date(2026, 9, 1))
    session.add(v)
    session.commit()

    q = session.query(Vacation).filter_by(p_id=sample_participant.p_id).first()
    assert q is not None
    assert q.vacation_start == datetime.date(2026, 1, 1)
    assert q.vacation_end == datetime.date(2026, 9, 1)
    assert q.participant == sample_participant


def test_delete_vacation(session, vacation_factory, sample_participant):
    v = vacation_factory()
    session.add(v)
    session.commit()
    session.delete(v)
    session.commit()

    assert (
        session.query(Vacation).
        filter_by(
            p_id=sample_participant.p_id,
            vacation_start=datetime.date(2026, 1, 1),
        )
        .first()
        is None
    )

#endregion: CRUD-Tests