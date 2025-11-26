from xml.sax.handler import property_interning_dict

import pytest
from datetime import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.vacation_model import Vacation
from lib.models.participant_model import Participant
from lib.database import BaseClass



def test_create_vacation(session):
    vacation = Vacation(
        p_id = Participant.p_id,
        vacation_start = datetime(2023, 1, 1),
        vacation_end =datetime(2023, 1, 31)
    )
    session.add(vacation)
    session.commit()

    query = session.query(vacation).filter_by(p_id= Participant.p_id ).first()

    assert query is not None
    assert query.p_id == Participant.p_id
    assert query.vacation_start == datetime.date(2023, 1, 1)
    assert query.vacation_en == datetime.date(2023, 1, 31)

