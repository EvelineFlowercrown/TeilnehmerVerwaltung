from typing import List
from datetime import date
from enum import Enum

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum

from lib.database import BaseClass


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
    internship_start: Mapped[date] = mapped_column(Date, primary_key=True)
    internship_end: Mapped[date] = mapped_column(Date, nullable=False)

    btz_day: Mapped[BtzDay] = mapped_column(
        SQLEnum(BtzDay, name="btz_day_enum"), nullable=False
    )

    participant: Mapped["Participant"] = relationship(
        back_populates="internships"
    )
