from sqlalchemy import Column, from sqlalchemy import Column, String, Integer, Date, Boolean, event,ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from lib.database import BaseClass as Base
from datetime import timedelta
from typing import List
#-----------------------------------------------------------------------------------------------------------------------
#Kitchen Duty part off: - participants 1: N assignment - kitchen_duty 1: N assignment
#----------------------------------------------------------------------------------------------------------------------
class KitchenDuty(Base):
    __tablename__ = "kitchen_dutys_table"

    kd_id: Mapped[str] = mapped_column(
        primary_key = True
    )

    kd_start: Mapped[Date] = mapped_column(
        nullable = False
    )

     # Event Listener before_insert in KitchenDuty
    @event.listens_for(KitchenDuty, "before_insert")
    def set_kd_end(mapper, connection, target):
        if target.kd_start and not target.kd_end:
            target.kd_end = target.kd_start + timedelta(days=5)

    kd_end: Mapped[Date] = mapped_column(
        nullable = True
    )

    participants: Mapped[List["Participant"]] = relationship(
        secondary = assignments_table,
        back_populates = "kitchen_duties"
        )
    # -------------------------
    # REPR
    # -------------------------
    def __repr__(self) -> str:
        return (
            f"<KitchenDuty(kd_id={self.kd_id}, "
            f"start={self.kd_start}, end={self.kd_end})>"
        )String, Integer, Date, Boolean, event,ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from database import BaseClass
from datetime import timedelta
from typing import List
#-----------------------------------------------------------------------------------------------------------------------
#Kitchen Duty part off: - participants 1: N assignment - kitchen_duty 1: N assignment
#----------------------------------------------------------------------------------------------------------------------
class KitchenDuty(Base):
    __tablename__ = "kitchen_dutys_table"

    kd_id: Mapped[str] = mapped_column(
        primary_key = True
    )

    kd_start: Mapped[Date] = mapped_column(
        nullable = False
    )

     # Event Listener before_insert in KitchenDuty
    @event.listens_for(KitchenDuty, "before_insert")
    def set_kd_end(mapper, connection, target):
        if target.kd_start and not target.kd_end:
            target.kd_end = target.kd_start + timedelta(days=5)

    kd_end: Mapped[Date] = mapped_column(
        nullable = True
    )

    participants: Mapped[List["Participant"]] = relationship(
        secondary = assignments_table,
        back_populates = "kitchen_duties"
        )
    # -------------------------
    # REPR
    # -------------------------
    def __repr__(self) -> str:
        return (
            f"<KitchenDuty(kd_id={self.kd_id}, "
            f"start={self.kd_start}, end={self.kd_end})>"
        )