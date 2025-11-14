# main.py
import importer
import models
from database import  engine,session
from models import *

# Tabellen erzeugen
BaseClass.metadata.create_all(bind=engine)

import_order = {
    "data/bt_mitarbeiter.csv":models.BT_Mitarbeiter,
    "data/ps_mitarbeiter.csv":models.PS_Mitarbeiter,
    "data/teilnehmende.csv":models.Teilnehmender,
    "data/Praktikum.csv":models.Praktikum,
}


#for path in import_order.keys():
#    importer.import_csv_to_table(path,import_order[path])


teilnehmer = session.get(Teilnehmender, 69)

print(teilnehmer.bt_mitarbeiter.vorname)