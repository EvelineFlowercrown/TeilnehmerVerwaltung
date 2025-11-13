from pathlib import Path
from lib.databaseProvider import DatabaseProvider
DATA_DIR = Path(__file__).parent.parent / "data"


def setup_database_from_txt():
    """Erstellt Tabellen in der SQLite-DB anhand aller .txt-Dateien in data/."""
    db = DatabaseProvider()
    db.connect()

    #check if Data Directory exists
    if not DATA_DIR.exists():
        print("❌ Verzeichnis 'data/' nicht gefunden.")
        return

    #find all txt files
    txt_files = sorted(DATA_DIR.glob("*.txt"))
    if not txt_files:
        print("⚠️ Keine .txt-Dateien gefunden.")
        return

    #iterate over all txt files
    for file in txt_files:
        table_name = file.stem  # Dateiname ohne .txt

        try:
            with open(file, "r", encoding="utf-8") as f:
                line = f.readline().strip()

        except Exception as e:
            print(f"❌ Fehler beim Lesen von {file.name}: {e}")
            continue

        if not line:
            print(f"⚠️ Datei {file.name} ist leer – übersprungen.")
            continue

        columns = [col.strip() for col in line.split(",") if col.strip()]
        if not columns:
            print(f"⚠️ Keine gültigen Spaltennamen in {file.name}.")
            continue

        # Jede Spalte wird als TEXT-Typ definiert
        column_defs = [(col, "TEXT") for col in columns]

        print(f"🧱 Erstelle Tabelle '{table_name}' mit Spalten: {', '.join(columns)}")
        db.create_table(table_name, column_defs)

    db.close()
    print("✅ Setup abgeschlossen.")


if __name__ == "__main__":
    setup_database_from_txt()
