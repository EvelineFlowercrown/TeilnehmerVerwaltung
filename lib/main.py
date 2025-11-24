# main.py
import random

from sqlalchemy import select
from lib import models, importer
from lib.database import engine, BaseClass, SessionLocal

# Tabellen erzeugen
BaseClass.metadata.create_all(bind=engine)
# Session Starten
session = SessionLocal()


def import_mock_data():
    import_order = {
        "../data/ps_staff_table.csv": models.PsStaff,
        "../data/pt_staff_table.csv": models.PtStaff,
        "../data/participant_table.csv": models.Participant,
        "../data/internship_table.csv": models.Internship,
        "../data/vacation_table.csv": models.Vacation,
        "../data/kitchen_duty_table.csv": models.KitchenDuty,
    }

    # CSVs laden
    for path, model in import_order.items():
        importer.import_csv_to_table(path, model)

    # Alle Datensätze holen
    participants = session.scalars(select(models.Participant)).all()
    duties = session.scalars(select(models.KitchenDuty)).all()

    # Für jeden Küchendienst 3 zufällige Teilnehmer (ohne Duplikate)
    for kd in duties:
        picked = random.sample(
            participants, 3
        )  # garantiert 3 unterschiedliche Teilnehmer
        kd.participants.extend(picked)

    session.commit()


# import_mock_data()


# beispielmethode zur datenabfrage
def wer_wie_oft_küchendienst():
    all_users = session.scalars(select(models.Participant)).all()
    for user in all_users:
        print(
            f"{user.first_name + ' ' + user.surname} has performed {len(user.kitchen_duties)} kitchen duties."
        )


wer_wie_oft_küchendienst()
