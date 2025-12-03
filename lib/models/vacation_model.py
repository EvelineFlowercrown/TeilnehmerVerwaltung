from typing import List
from datetime import date

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from lib.database import BaseClass
from .participant_model import Participant



class Vacation(BaseClass):
    __tablename__ = "vacation_table"

    p_id: Mapped[int] = mapped_column(
        ForeignKey("participant_table.p_id"),
        primary_key=True,
    )
    vacation_start: Mapped[date] = mapped_column(
        Date,
        primary_key=True,
    )
    vacation_end: Mapped[date] = mapped_column(Date, nullable=False)

    participant: Mapped["Participant"] = relationship(
        back_populates="vacations"
    )
