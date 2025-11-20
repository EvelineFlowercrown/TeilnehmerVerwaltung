"""Models related to internship scheduling and BTZ attendance."""

from typing import List
from datetime import date
from enum import Enum

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum

from lib.database import BaseClass


class BtzDay(Enum):
    """Valid BTZ attendance days."""

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"


class Internship(BaseClass):
    """Internship entry linked to a participant."""

    __tablename__ = "internships_table"

    p_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"),
        primary_key=True,
        nullable=False,
    )
    internship_start: Mapped[date] = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
    )
    internship_end: Mapped[Date] = mapped_column(Date, nullable=False)
    btz_day: Mapped[BtzDay] = mapped_column(
        SQLEnum(BtzDay, name="btz_day"), nullable=False
    )

    participant: Mapped["Participant"] = relationship(back_populates="internships")
