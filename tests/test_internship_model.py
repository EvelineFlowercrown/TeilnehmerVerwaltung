import pytest
import datetime
from lib.models.internship_model import Internship


# region: Internship-Factory

# ---------------------------------------------------------
# Internship-Factory
# ---------------------------------------------------------
@pytest.fixture
def internship_factory(sample_participant):
    """
    Erzeugt eine Internship-Instanz für CRUD-Tests.
    Parameter können überschrieben werden.
    """
    def _factory(
        start=datetime.date(2026, 1, 30),
        end=datetime.date(2026, 2, 1),
        btz_day=Internship.BtzDay.MONDAY
    ):
        return Internship(
            p_id=sample_participant.p_id,
            internship_start=start,
            internship_end=end,
            btz_day=btz_day,
        )
    return _factory

# endregion: Internship-Factory

# region: Crud-Tests

# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def test_internship_create(session, internship_factory):
    internship = internship_factory()
    session.add(internship)
    session.commit()

    stored = (
        session.query(Internship)
        .filter_by(p_id=internship.p_id, internship_start=internship.internship_start)
        .first()
    )

    assert stored is not None
    assert stored.internship_end == datetime.date(2026, 2, 1)
    assert stored.btz_day == Internship.BtzDay.MONDAY


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------
def test_internship_read(session, internship_factory):
    internship = internship_factory()
    session.add(internship)
    session.commit()

    stored = (
        session.query(Internship)
        .filter_by(p_id=internship.p_id, internship_start=internship.internship_start)
        .first()
    )

    assert stored is not None
    assert stored.internship_end == datetime.date(2026, 2, 1)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
def test_internship_update(session, internship_factory):
    internship = internship_factory()
    session.add(internship)
    session.commit()

    internship.internship_end = datetime.date(2026, 4, 15)
    internship.btz_day = Internship.BtzDay.FRIDAY
    session.commit()

    updated = (
        session.query(Internship)
        .filter_by(p_id=internship.p_id, internship_start=internship.internship_start)
        .first()
    )

    assert updated.internship_end == datetime.date(2026, 4, 15)
    assert updated.btz_day == Internship.BtzDay.FRIDAY


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
def test_internship_delete(session, internship_factory):
    internship = internship_factory()
    session.add(internship)
    session.commit()

    session.delete(internship)
    session.commit()

    deleted = (
        session.query(Internship)
        .filter_by(p_id=internship.p_id, internship_start=internship.internship_start)
        .first()
    )

    assert deleted is None

# endregion: Crud-Tests


# ---------------------------------------------------------
# INVALID ENUM
# ---------------------------------------------------------
def test_internship_invalid_btz_day_raises(session, internship_factory):
    with pytest.raises(ValueError):
        internship = internship_factory(btz_day="SUNDAY")  # ungültig
        session.add(internship)
        session.commit()
