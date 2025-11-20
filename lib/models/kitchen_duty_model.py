import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from lib.database import BaseClass as Base
from typing import List


# -----------------------------------------------------------------------------------------------------------------------
# Kitchen Duty part off: - participants 1: N assignment - kitchen_duty 1: N assignment
# ----------------------------------------------------------------------------------------------------------------------
class KitchenDuty(Base):
    __tablename__ = "kitchen_duties_table"

    kd_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kd_start: Mapped[datetime.date] = mapped_column(nullable=False)
    kd_end: Mapped[datetime.date] = mapped_column(nullable=True)

    # M2M over association table
    participants: Mapped[List["Participant"]] = relationship(
        secondary="assignment_table",
        back_populates="kitchen_duties"
    )

    # Missing piece → needed for Assignment.back_populates="kitchen_duty"
    assignments: Mapped[List["Assignment"]] = relationship(
        back_populates="kitchen_duty"
    )

    def __repr__(self):
        return f"<KitchenDuty(kd_id={self.kd_id}, start={self.kd_start}, end={self.kd_end})>"
