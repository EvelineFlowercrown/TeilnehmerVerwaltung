from typing import List
from datetime import date
from enum import Enum

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, validates
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

    @validates("btz_day")
    def validate_BtzDay(self, key,  value):
        # key == "measure"

        # Wenn bereits ein Enum-Objekt übergeben wird
        if isinstance(value, Internship.BtzDay):
            return value

        # Strings o.ä. in das Enum umwandeln
        try:
            return Internship.BtzDay(value)
        except ValueError as error:
            # Genau das sollte dein Test mit pytest.raises(ValueError) abfangen
            raise ValueError(f"Ungültiger Wert für BtzDay: {value!r}") from error

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
