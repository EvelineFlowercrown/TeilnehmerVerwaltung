from nicegui import ui
from lib.layout import app_layout
from lib.database import SessionLocal
from lib.models import Participant  # ORM Klasse


def page_home():
    """Startseite – enthält eine Tabelle der Participants."""
    print("page_home wird aufgerufen")  # Debug

    def load_participants():

        print("load_participants wird aufgerufen")  # Debug
        db = SessionLocal()
        try:
            return db.query(Participant).all()
        finally:
            db.close()

    data = load_participants()
    print(f"Geladene Daten: {len(data)} Einträge")  # Debug

    def build_content():
        print("build_content wird aufgerufen")  # Debug
        ui.label("Participants").classes("text-2xl mb-4")

        # Tabelle erzeugen
        ui.table(
            columns=[
                {'name': 'p_id', 'label': 'ID', 'field': 'p_id'},
                {'name': 'surname', 'label': 'Nachname', 'field': 'surname'},
                {'name': 'first_name', 'label': 'Vorname', 'field': 'first_name'},
                {'name': 'btz_start', 'label': 'Start', 'field': 'btz_start'},
                {'name': 'btz_ende', 'label': 'Ende', 'field': 'btz_ende'},
            ],
            rows=[{
                'p_id': p.p_id,
                'surname': p.surname,
                'first_name': p.first_name,
                'btz_start': p.btz_start,
                'btz_ende': p.btz_ende,
            } for p in data],
            row_key='p_id'
        ).classes('w-full')

    # Funktion übergeben (nicht aufrufen!)
    app_layout(build_content)