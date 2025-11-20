# participant_model.py
import datetime
from enum import Enum
from typing import List

from lib.database import BaseClass
from sqlalchemy import (
    Date,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Participant(BaseClass):
    __tablename__ = "participant_table"

    p_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    surname: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)

    btz_start: Mapped[datetime.date] = mapped_column(nullable=False)
    btz_ende: Mapped[datetime.date] = mapped_column(nullable=False)

    pt_id: Mapped[int] = mapped_column(ForeignKey("pt_staff_table.pt_id"))
    ps_id: Mapped[int] = mapped_column(ForeignKey("ps_staff_table.ps_id"))

    gdb: Mapped[bool] = mapped_column(nullable=True)
    bvb: Mapped[bool] = mapped_column(nullable=True)
    seat: Mapped[int] = mapped_column(nullable=True)
    initials: Mapped[str] = mapped_column(nullable=True)
    table: Mapped[int] = mapped_column(nullable=True)

    class Measure(Enum):
        BT = "BT"
        BVB = "BVB"
        FSM = "FSM"
        KIM = "KIM"

    measure: Mapped["Participant.Measure"] = mapped_column(
        SQLEnum(Measure, name="measure_enum"), nullable=False
    )

    birthday: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    class BirthdayList(Enum):
        JA = "Ja"
        NEIN = "Nein"
        KARTE = "Karte"

    birthday_list: Mapped["Participant.BirthdayList"] = mapped_column(
        SQLEnum(BirthdayList, name="birthday_list_enum"),
        nullable=True
    )

    assignments: Mapped[List["Assignment"]] = relationship(back_populates="participant")
    kitchen_duties: Mapped[List["KitchenDuty"]] = relationship(
        secondary="assignment_table",
        back_populates="participants"
    )
    internships: Mapped[List["Internship"]] = relationship(back_populates="participant")
    vacations: Mapped[List["Vacation"]] = relationship(back_populates="participant")

    ps_staff: Mapped["PsStaff"] = relationship(back_populates="participants")
    pt_staff: Mapped["PtStaff"] = relationship(back_populates="participants")

    def __repr__(self):
        return f"<Participant(p_id={self.p_id}, name='{self.first_name} {self.surname}', measure={self.measure.value})>"

