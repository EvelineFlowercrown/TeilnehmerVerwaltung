# from enum import Enum
from typing import List

# from sqlalchemy import Integer, ForeignKey, String
# from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from lib.database import BaseClass


class PsStaff(BaseClass):
    __tablename__ = "ps_staff_table"

    ps_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    participants: Mapped[List["Participant"]] = relationship(
        back_populates="ps_staff"
    )

    def __repr__(self):
        return (f"{self.first_name} {self.surname}")

