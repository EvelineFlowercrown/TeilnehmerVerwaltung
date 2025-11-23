from enum import Enum
from typing import List

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from database import BaseClass


class PtStaff(BaseClass):
    __tablename__ = "pt_staff_table"

    pt_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name_pt: Mapped[str] = mapped_column(nullable=False)
    surname_pt: Mapped[str] = mapped_column(nullable=False)

    participants: Mapped[List["Participant"]] = relationship(back_populates="pt_staff")
