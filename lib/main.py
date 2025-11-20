# main.py
from lib import importer
import lib.models as models
from lib.database import engine, BaseClass, SessionLocal


# Tabellen erzeugen
BaseClass.metadata.create_all(bind=engine)

import_order = {
    "../data/ps_staff_table.csv":models.PsStaff,
    "../data/pt_staff_table.csv":models.PtStaff,
    "../data/participant_table.csv":models.Participant,
    "../data/internship_table.csv":models.Internship,
    "../data/vacation_table.csv":models.Vacation,
    "../data/assignment_table.csv":models.Assignment,
    "../data/kitchen_duty_table.csv":models.KitchenDuty
}


for path in import_order.keys():
   importer.import_csv_to_table(path,import_order[path])


session = SessionLocal()

