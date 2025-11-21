from sqlalchemy import Table, Column, ForeignKey, Integer
from lib.database import BaseClass as Base

assignment_table = Table(
    "assignment_table",
    Base.metadata,
    Column("p_id", Integer, ForeignKey("participant_table.p_id"), primary_key=True),
    Column("kd_id", Integer, ForeignKey("kitchen_duties_table.kd_id"), primary_key=True),
)
