from re import search
from nicegui import ui
from lib.layout import app_layout
from lib.database import SessionLocal
from lib.models import Participant
from sqlalchemy import or_, String, Enum


def page_home():
    print("page_home wird aufgerufen")

    def load_participants(model, search: str | None = None):
        """Lädt Participants, optional mit substring-Filtern."""
        db = SessionLocal()
        try:
            query = db.query(Participant)

            if search and search.strip():
                search_pattern = f"%{search}%"
                filters = []

                for column in model.__table__.columns:
                    # Nur String-Spalten durchsuchen
                    if isinstance(column.type, String) and not isinstance(column.type, Enum):
                        filters.append(column.ilike(search_pattern))

                # HIER DAS PROBLEM: Liste entpacken mit *
                if filters:
                    query = query.filter(or_(*filters))

            return query.all()

        finally:
            db.close()

    def to_dict(model, excluded_columns):
        excluded_columns = excluded_columns or []
        return {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
            if column.name not in excluded_columns
        }

    def buildLayout(model, excluded_columns, search_value=None):
        # Tabellenlayout erzeugen
        rows = [to_dict(participant, excluded_columns)
                for participant in load_participants(model, search_value)]

        # Spalten aus den verbleibenden Keys erstellen (wenn es Daten gibt)
        if rows:
            columns = [
                {
                    'name': column,
                    'label': column.replace("_", " ").title(),
                    'field': column,
                    'sortable': True
                }
                for column in rows[0].keys()
            ]
        else:
            # Fallback: Alle Spalten außer excluded_columns
            all_columns = [column.name for column in model.__table__.columns
                           if column.name not in excluded_columns]
            columns = [
                {
                    'name': column,
                    'label': column.replace("_", " ").title(),
                    'field': column,
                    'sortable': True
                }
                for column in all_columns
            ]

        return rows, columns

    def build_content():
        print("build_content wird aufgerufen")

        # Variablen als Dictionary speichern, damit sie in Closures verfügbar sind
        state = {
            'excluded_columns': [],
            'search_value': None,
            'column_checkboxes': {},
            'table': None
        }

        def update_table():
            """Aktualisiert die Tabelle basierend auf excluded_columns und search_value"""
            if state['table']:
                rows, cols = buildLayout(Participant,
                                         state['excluded_columns'],
                                         state['search_value'])
                state['table'].rows = rows
                state['table'].columns = cols

        def handle_checkbox_change(column_name, value):
            """Handler für Checkbox-Änderungen"""
            if not value and column_name not in state['excluded_columns']:
                state['excluded_columns'].append(column_name)
            elif value and column_name in state['excluded_columns']:
                state['excluded_columns'].remove(column_name)
            update_table()

        def handle_search_change(suche):
            """Handler für Suchfeld-Änderungen"""
            state['search_value'] = suche.value if suche.value else None
            update_table()

        # Initiale Daten laden
        rows, cols = buildLayout(Participant, state['excluded_columns'], state['search_value'])

        with ui.column().classes("w-full mb-6"):
            # Erste Zeile: Überschrift + Settings
            with ui.row().classes("items-center w-full mb-2"):
                ui.label("Participants").classes("text-2xl font-bold mr-2")

                # Settings Dropdown mit Tooltip
                with ui.dropdown_button(icon="settings", color="grey-7").props("flat round dense"):
                    with ui.card().classes("p-3 w-56"):
                        ui.label("Spalten anzeigen").classes("font-bold mb-3 text-primary")
                        # Checkboxen für alle Spalten erstellen
                        for column in Participant.__table__.columns:
                            column_name = column.name
                            checkbox = ui.checkbox(
                                column_name.replace("_", " ").title(),
                                value=column_name not in state['excluded_columns'],
                                on_change=lambda e, col=column_name: handle_checkbox_change(col, e.value)
                            ).classes("w-full")
                            state['column_checkboxes'][column_name] = checkbox

            # Zweite Zeile: Suchfeld
            with ui.row().classes("w-full justify-end"):
                with ui.input(
                        placeholder="Suche nach Name, kürzel, etc...",
                        on_change=lambda e: handle_search_change(e)
                ).props("clearable dense outlined prefix=search").classes("w-80"):
                    ui.tooltip("Durchsucht alle Text-Spalten")

        # Tabelle erstellen
        state['table'] = ui.table(
            rows=rows,
            columns=cols,
            row_key='p_id',
            pagination=10
        ).classes('w-full shadow-sm')

    app_layout(build_content)