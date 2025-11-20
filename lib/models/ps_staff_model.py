from enum import Enum
from typing import List

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from database import BaseClass


class PsFirstName(Enum):
    PETRA = "Petra"
    ANJA_KATHARINA = "Anja Katharina"
    MELANIE = "Melanie"
    CORINNA = "Corinna"
    JOERG = "Jörg"
    LISA = "Lisa"
    BEATE = "Beate"
    MARCUS = "Marcus"
    LEONY = "Leony"


class PsSurname(Enum):
    BAUMGARTEN = "Baumgarten"
    VON_BLOMBERG = "von Blomberg"
    BRIER = "Brier"
    GROSS = "Groß"
    HARMJANZ = "Harmjanz"
    KLEIDER = "Kleider"
    SCHUETT = "Schütt"
    THOMSEN = "Thomsen"
    WOLLIK = "Wollik"


class PsStaff(BaseClass):
    __tablename__ = "ps_staff_table"
    ps_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"),
        primary_key=True,
        nullable=False,
    )
    first_name_ps: Mapped[PsFirstName] = mapped_column(
        SQLEnum(PsFirstName, name="pt_first_name_enum"), nullable=False
    )
    surname_ps: Mapped[PsSurname] = mapped_column(
        SQLEnum(PsSurname, name="ps_surname_enum"), nullable=False
    )

    participants: Mapped[List["Participant"]] = relationship(
        back_populates="ps_staff"
    )
