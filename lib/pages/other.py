import importlib

from nicegui import ui
from lib.layout import app_layout

def page_other():

    def get_all_models():
        try:
            models_module = importlib.import_module('lib.models')
            models = []
            for name in dir(models_module):
                obj = getattr(models_module, name)
                try:
                    if hasattr(obj, '__table__') and hasattr(obj.__table__, 'columns'):
                        models.append(obj)
                except:
                    continue
            return models
        except Exception as e:
            print(f"Fehler beim Laden der Modelle: {e}")
            # Fallback zu manueller Liste
            from lib.models import Participant, KitchenDuty, Internship, Vacation, PsStaff, PtStaff
            return [Participant, KitchenDuty, Internship, Vacation, PsStaff, PtStaff]

    AVAILABLE_MODELS = get_all_models()

    def build_content():
        state = {
            'current_model': AVAILABLE_MODELS[0] if AVAILABLE_MODELS else None,
            'excluded_columns': [],
            'search_value': None,
            'table': None,
            'model_select': None,
            'search_input': None,
            'column_checkboxes': {},
            'table_container': None
        }

        def handle_model_change(model_class):
            """Handler für Modellwechsel."""
            state['current_model'] = model_class

            # Alle Spalten mit "_id" im Namen standardmäßig ausschließen
            state['excluded_columns'] = [
                column.name for column in model_class.__table__.columns
                if '_id' in column.name
            ]

            state['search_value'] = None

            # Suchfeld zurücksetzen
            if state['search_input']:
                state['search_input'].value = ''


            ui.notify(f"Modell gewechselt zu: {model_class.__name__}")

        # UI-Aufbau
        with ui.column().classes("w-full mb-6"):
            # Kopfzeile mit Modellauswahl und Suchfeld
            with ui.row().classes("items-center w-full mb-4 justify-between"):
                # Linke Seite: Titel + Modellauswahl
                with ui.row().classes("items-center gap-4"):
                    ui.label("Datenbank Browser").classes("text-2xl font-bold")

                    # Modellauswahl Dropdown
                    if AVAILABLE_MODELS:
                        state['model_select'] = ui.select(
                            options={model: model.__name__ for model in AVAILABLE_MODELS},
                            value=state['current_model'],
                            on_change=lambda e: handle_model_change(e.value),
                            label="Modell"
                        ).classes("w-48")
                    else:
                        ui.label("Keine Modelle gefunden").classes("text-red")

                # Rechte Seite: Suchfeld + Settings
                with ui.row().classes("items-center gap-2"):
                    # Suchfeld
                    state['search_input'] = ui.input(
                        placeholder="Suche...",
                        on_change=lambda e: print(e.value)
                    ).props("dense outlined clearable").classes("w-64")

    app_layout(build_content)
