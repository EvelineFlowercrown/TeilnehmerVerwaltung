from datetime import date
from enum import Enum
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Enum as SQLEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from lib.database import BaseClass
from .participant_model import Participant


class Internship(BaseClass):
    __tablename__ = "internships_table"

    class BtzDay(Enum):
        """Valid BTZ attendance days."""

        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"

    p_id: Mapped[int] = mapped_column(
        ForeignKey("participant_table.p_id"),
        primary_key=True,
    )
    internship_start: Mapped[date] = mapped_column(
        Date,
        primary_key=True,
        nullable=False
    )

    internship_end: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    btz_day: Mapped["BtzDay"] = mapped_column(  # ✅ String-Zitat für Forward-Ref
        SQLEnum(BtzDay, name="btz_day_enum"),
        nullable=False
    )

    participant: Mapped["Participant"] = relationship(
        back_populates="internships"
    )
