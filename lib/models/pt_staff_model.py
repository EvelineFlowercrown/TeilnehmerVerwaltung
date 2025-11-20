from enum import Enum
from typing import List

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

    participants: Mapped[List["Participant"]] = relationship(
        back_populates="ps_staff"
    )
