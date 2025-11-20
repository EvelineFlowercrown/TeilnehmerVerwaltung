from sqlalchemy import String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from lib.database import BaseClass as Base
from typing import List


# -------------------------------------------------------------------------------------------------------------------
# Assignment part off: - participants 1: N assignment - kitchen_duty 1: N assignment
# --------------------------------------------------------------------------------------------------------------------
class Assignment(Base):
    __tablename__ = "assignment_table"
    p_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"), primary_key=True, nullable=False
    )
    kd_id: Mapped[int] = mapped_column(
        ForeignKey("kitchen_dutys_table.ki_id"),
        primary_key=True,
        nullable=False,
    )
    participants: Mapped["Participant"] = relationship(back_populates="assignments")
    kitchen_duties: Mapped["KitchenDuty"] = relationship(back_populates="assignments")

    # -----------------------------------
    # REPR
    # -----------------------------------
    def __repr__(self) -> str:
        return f"<Assignment(p_id={self.p_id}, kd_id={self.kd_id})>"
