# participant_model.py
import datetime
from enum import Enum
from lib.database import BaseClass
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Boolean,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Participants(BaseClass):
    __tablename__ = "participant_table"

    p_id: Mapped[int] = mapped_column(
        nullable=False, primary_key=True, autoincrement=True
    )

    # Name Sur and First and GDB; not Null
    surname: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)

    # ----------------------------------------------------------------------------------------------------------------------
    # Start End Measure
    # ----------------------------------------------------------------------------------------------------------------------
    btz_start: Mapped[datetime.date] = mapped_column(nullable=False)
    btz_ende: Mapped[datetime.date] = mapped_column(nullable=False)

    # ----------------------------------------------------------------------------------------------------------------------
    # Staff Professional-Trainer and Psychosocial-Trainer
    # -----------------------------------------------------------------------------------------------------------------------
    pt_id: Mapped[int] = mapped_column(ForeignKey("pt_staff.pt_id"))
    ps_id: Mapped[int] = mapped_column(ForeignKey("ps_staff.ps_id"))

    # -----------------------------------------------------------------------------------------------------------------------
    # Needs
    # -----------------------------------------------------------------------------------------------------------------------
    gdb: Mapped[bool] = mapped_column(nullable=True)
    bvb: Mapped[bool] = mapped_column(nullable=True)
    seat: Mapped[int] = mapped_column(nullable=True)
    initials: Mapped[str] = mapped_column(nullable=True)
    table: Mapped[int] = mapped_column(nullable=True)

    # Enum for Measure
    class Measure(Enum):
        BT = "BT"
        BVB = "BVB"
        FSM = "FSM"
        KIM = "KIM"

    measure: Mapped[Measure] = mapped_column(
        SQLEnum(Measure, name="measure_enum"), nullable=False
    )

    # -----------------------------------------------------------------------------------------------------------------------
    # Birthdays
    # -----------------------------------------------------------------------------------------------------------------------
    birthday: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    class BirthdayList(Enum):
        JA = "Ja"
        NEIN = "Nein"
        KARTE = "Karte"

    birthday_list: Mapped[BirthdayList] = mapped_column(
        SQLEnum(BirthdayList, name="birthday_list_enum"), nullable=True
    )

    # -------------------------
    # REPR
    # -------------------------
    def __repr__(self) -> str:
        return (
            f"<Participants(p_id={self.p_id}, "
            f"name='{self.first_name} {self.surname}', "
            f"measure={self.measure.value})>"
        )
