import pytest

import datetime

from sqlalchemy.exc import InvalidRequestError

from lib.models.participant_model import Participant  # Importpfad
from lib.models import PsStaff, PtStaff


def test_create_participant_minimal(session, sample_staff):
    participant = Participant(
        surname="Mustermann",
        first_name="Max",
        btz_start=datetime.date(2023, 1, 1),
        btz_end=datetime.date(2023, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )

    session.add(participant)
    session.commit()

    q = session.query(Participant).filter_by(surname="Mustermann").first()

    assert q is not None
    assert q.first_name == "Max"
    assert q.measure == Participant.Measure.KIM
    assert q.ps_staff.ps_id == sample_staff["ps"].ps_id
    assert q.pt_staff.pt_id == sample_staff["pt"].pt_id


def test_create_participant_missing_required_fields(session):
    """Erwartet: IntegrityError wegen fehlendem Pflichtfeld."""
    with pytest.raises(Exception):  # SQLAlchemy erzeugt IntegrityError
        p = Participant(
            surname="OhneVorname",
            # first_name fehlt
            btz_start=datetime.date(2023, 1, 1),
            btz_end=datetime.date(2023, 12, 31),
            measure=Participant.Measure.BT,
        )
        session.add(p)
        session.commit()


def test_create_invalid_enum(session, sample_staff):
    """Ungültige Enum-Werte sollten schon Python-seitig Fehler werfen."""
    with pytest.raises(ValueError):
        Participant(
            surname="Fail",
            first_name="Enum",
            btz_start=datetime.date(2023, 1, 1),
            btz_end=datetime.date(2023, 12, 31),
            measure="INVALID",  # ValueError
        )


# -----------------------
# endregion Tests: Update
# -----------------------


def test_update_nonexistent(session, sample_staff):
    """Update auf ein Objekt, das nicht existiert → SQLAlchemy merged es ein."""
    fake = Participant(
        p_id=999,  # erzwingen einer primären ID
        surname="Ghost",
        first_name="Nowhere",
        btz_start=datetime.date(2020, 1, 1),
        btz_end=datetime.date(2020, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )

    merged = session.merge(fake)  # SQLAlchemy fügt es ein!
    session.commit()

    assert merged.p_id is not None
    assert session.query(Participant).count() == 1


# -----------------------
# Tests: Delete
# -----------------------


def test_delete_participant(session, sample_staff):
    p = Participant(
        surname="Delete",
        first_name="Me",
        btz_start=datetime.date(2023, 1, 1),
        btz_end=datetime.date(2023, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )
    session.add(p)
    session.commit()

    session.delete(p)
    session.commit()

    assert session.query(Participant).count() == 0


def test_delete_twice(session, sample_staff):
    p = Participant(
        surname="Twice",
        first_name="Gone",
        btz_start=datetime.date(2024, 1, 1),
        btz_end=datetime.date(2024, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )
    session.add(p)
    session.commit()

    session.delete(p)
    session.commit()

    # Zweites Delete sollte stillschweigend ignoriert werden
    session.delete(p)
    session.commit()

    assert session.query(Participant).count() == 0


def test_delete_nonexistent(session, sample_staff):
    """Löschen eines nicht existierenden Objekts erzeugt eine InvalidRequestError Exception."""
    participant = Participant(
        p_id=777,
        surname="X",
        first_name="Y",
        btz_start=datetime.date(2020, 1, 1),
        btz_end=datetime.date(2020, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=sample_staff["ps"].ps_id,
        pt_id=sample_staff["pt"].pt_id,
    )
    # Objekt nie hinzugefügt
    with pytest.raises(InvalidRequestError):
        session.delete(participant)
        session.commit()


# -----------------------
# Tests: Relationships
# -----------------------


def test_relationship_staff_backpopulation(session, sample_staff):
    ps = sample_staff["ps"]
    pt = sample_staff["pt"]

    p = Participant(
        surname="Back",
        first_name="Pop",
        btz_start=datetime.date(2022, 1, 1),
        btz_end=datetime.date(2022, 12, 31),
        measure=Participant.Measure.KIM,
        ps_id=ps.ps_id,
        pt_id=pt.pt_id,
    )

    session.add(p)
    session.commit()

    assert p in ps.participants
    assert p in pt.participants


def test_change_relationship_references(session, sample_staff):
    ps1 = sample_staff["ps"]
    pt1 = sample_staff["pt"]

    ps2 = PsStaff(first_name="Erna", surname="Neu")
    pt2 = PtStaff(first_name="Lukas", surname="Neu")
    session.add_all([ps2, pt2])
    session.commit()

    p = Participant(
        surname="Switch",
        first_name="Test",
        btz_start=datetime.date(2023, 1, 1),
        btz_end=datetime.date(2023, 12, 31),
        measure=Participant.Measure.FSM,
        ps_id=ps1.ps_id,
        pt_id=pt1.pt_id,
    )
    session.add(p)
    session.commit()

    # Wechsel der Referenzen
    p.ps_staff = ps2
    p.pt_staff = pt2
    session.commit()

    assert p in ps2.participants
    assert p in pt2.participants
    assert p not in ps1.participants
    assert p not in pt1.participants
