# participant_model.py
import datetime
from enum import Enum
from typing import List , TYPE_CHECKING



if TYPE_CHECKING:
    from .internship_model import Internship
    from .vacation_model import Vacation
    from .kitchen_duty_model import KitchenDuty
    from .ps_staff_model import PsStaff
    from .pt_staff_model import PtStaff
    from .assignment_table import assignment_table



from lib.database import BaseClass

from sqlalchemy import (
    Date,table,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates



class Participant(BaseClass):
    __tablename__ = "participant_table"

    p_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    surname: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)

    btz_start: Mapped[datetime.date] = mapped_column(nullable=False)
    btz_end: Mapped[datetime.date] = mapped_column(nullable=False)

    pt_id: Mapped[int] = mapped_column(ForeignKey("pt_staff_table.pt_id"))
    ps_id: Mapped[int] = mapped_column(ForeignKey("ps_staff_table.ps_id"))

    gdb: Mapped[bool] = mapped_column(nullable=True)
    bvb: Mapped[bool] = mapped_column(nullable=True)
    seat: Mapped[int] = mapped_column(nullable=True)
    initials: Mapped[str] = mapped_column(nullable=True)
    table: Mapped[int] = mapped_column(nullable=True)

    # -------------------------------------------------
    # Measure-Enum
    # -------------------------------------------------
    class Measure(str, Enum):
        BT = "BT"
        BVB = "BVB"
        FSM = "FSM"
        KIM = "KIM"

    measure: Mapped["Participant.Measure"] = mapped_column(
        SQLEnum(Measure, name="measure_enum", native_enum=False, validate_strings=True),
        nullable=False,
    )

    @validates("measure")
    def validate_measure(self, value):
        # key == "measure"

        # Wenn bereits ein Enum-Objekt übergeben wird
        if isinstance(value, Participant.Measure):
            return value

        # Strings o.ä. in das Enum umwandeln
        try:
            return Participant.Measure(value)
        except ValueError as exc:
            # Genau das sollte dein Test mit pytest.raises(ValueError) abfangen
            raise ValueError(f"Ungültiger Wert für measure: {value!r}") from exc

    birthday: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    class BirthdayList(str, Enum):
        JA = "Ja"
        NEIN = "Nein"
        KARTE = "Karte"

    birthday_list: Mapped["Participant.BirthdayList"] = mapped_column(
        SQLEnum(BirthdayList, name="birthday_list_enum"),
        nullable=True,
    )
    assignments: Mapped[list["Assignment"]] = relationship(
        secondary="assignment_table",
        back_populates="participants"
    )
    kitchen_duties: Mapped[List["KitchenDuty"]] = relationship(
        "KitchenDuty",
        secondary="assignment_table",
        back_populates="participants"
    )
    internships: Mapped[List["Internship"]] = relationship(back_populates="participant")
    vacations: Mapped[List["Vacation"]] = relationship(back_populates="participant")

    ps_staff: Mapped["PsStaff"] = relationship(back_populates="participants")
    pt_staff: Mapped["PtStaff"] = relationship(back_populates="participants")

    def __repr__(self):
        return (
            f"<Participant(p_id={self.p_id}, "
            f"name='{self.first_name} {self.surname}', "
            f"measure={self.measure.value})>"
        )
