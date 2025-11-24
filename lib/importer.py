import csv
import datetime
from datetime import date

from sqlalchemy import inspect, Date, Integer, Boolean

from lib.database import SessionLocal


# Hilfsfunktion: Datum erkennen
def try_parse_date(value: str) -> date | None:
    if not value or value.strip() == "":
        return None

    value = value.strip()
    formats = [
        "%Y/%m/%d",  # 2025/01/11
        "%m/%d/%Y",  # 1/11/2025
        "%d/%m/%Y",  # 11/01/2025
        "%Y-%m-%d",  # ISO
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    raise ValueError(f"Unbekanntes Datumsformat: {value}")


def import_csv_to_table(csv_path: str, model_class):
    Session = SessionLocal()
    """
    Importiert eine CSV in das SQLAlchemy-Modell.
    Die erste Zeile der CSV MUSS die Spaltennamen enthalten.
    """
    inspector = inspect(model_class)
    model_columns = {c.key: c for c in inspector.columns}

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0

        for row in reader:
            obj = model_class()

            for col_name, raw_value in row.items():

                if col_name not in model_columns:
                    print(
                        f"⚠️ Spalte '{col_name}' existiert nicht im Modell {model_class.__name__}."
                    )
                    continue

                column = model_columns[col_name]
                value = raw_value.strip()

                # Datentypen automatisch konvertieren
                if value == "":
                    value = None
                elif isinstance(column.type, Date):
                    value = try_parse_date(value)
                elif isinstance(column.type, Integer):
                    value = int(value)
                elif isinstance(column.type, Boolean):
                    value = value.lower() in ("1", "true", "yes", "ja")

                setattr(obj, col_name, value)

            Session.add(obj)
            count += 1

        Session.commit()

    print(
        f"📥 {count} Datensätze erfolgreich in Tabelle '{model_class.__tablename__}' importiert."
    )
