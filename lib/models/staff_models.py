from enum import Enum
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from database import BaseClass


class PtFirstName(Enum):
    NELLY = "Nelly"
    ANDREAS = "Andreas"
    LAURA_SOPHIE = "Laura-Sophie"
    FRANK = "Frank"
    STEFANIE = "Stefanie"
    ANDREA = "Andrea"


class PtSurname(Enum):
    FALK = "Falk"
    HARDER = "Harder"
    KELLER = "Keller"
    LEORNHARD = "Leonhardt"
    LOBES = "Lobes"
    REHME = "Rehme"


class PtStaff(BaseClass):
    __tablename__ = "pt_staff_table"

    pt_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"),
        primary_key=True,
        nullable=False,
    )
    first_name_ps: Mapped[PtFirstName] = mapped_column(
        SQLEnum(PtFirstName, name="pt_firstname_enum"), nullable=False
    )
    surname_ps: Mapped[PtSurname] = mapped_column(
        SQLEnum(PtSurname, name="pt_surname_enum"), nullable=False
    )

    participants: Mapped["Participant"] = relationship(
        back_populates="ps_staff"
    )


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

    participants: Mapped["Participant"] = relationship(
        back_populates="ps_staff"
    )
