from nicegui import ui
from lib.layout import app_layout
from lib.database import SessionLocal
from sqlalchemy import or_, String, Enum, inspect
from sqlalchemy.orm import joinedload, selectinload
import importlib


def page_home():
    print("page_home wird aufgerufen")

    # Dynamisch alle Modelle aus lib.models importieren
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

    def load_data(model, search: str | None = None):
        """Lädt Daten für ein Modell, optional mit substring-Filtern."""
        db = SessionLocal()
        try:
            query = db.query(model)

            # Eager Loading für ALLE Relationships erzwingen
            inspector = inspect(model)
            for rel_name in inspector.relationships.keys():
                # Für Collections selectinload, für einzelne Relationships joinedload
                rel = inspector.relationships[rel_name]
                if rel.uselist:  # Collection (One-to-Many, Many-to-Many)
                    query = query.options(selectinload(getattr(model, rel_name)))
                else:  # Single object (Many-to-One, One-to-One)
                    query = query.options(joinedload(getattr(model, rel_name)))

            # Suchlogik
            if search and search.strip():
                search_pattern = f"%{search}%"
                filters = []

                for column in model.__table__.columns:
                    if isinstance(column.type, String) and not isinstance(column.type, Enum):
                        filters.append(column.ilike(search_pattern))

                if filters:
                    query = query.filter(or_(*filters))

            return query.all()
        finally:
            db.close()

    def get_relationship_value(obj, rel_name):
        """Holt den Anzeigewert für eine Relationship."""
        try:
            related_obj = getattr(obj, rel_name)
            if related_obj is None:
                return None

            # Falls es eine Collection ist, nur die Anzahl zurückgeben
            if isinstance(related_obj, list):
                return len(related_obj)

            # Für einzelne Objekte: __repr__ oder andere Attribute
            if hasattr(related_obj, '__repr__'):
                # Die __repr__ Methode aufrufen und den String zurückgeben
                repr_str = repr(related_obj)
                # Entferne die spitzen Klammern, falls vorhanden
                if repr_str.startswith('<') and repr_str.endswith('>'):
                    repr_str = repr_str[1:-1]
                # Kürze sehr lange Strings
                if len(repr_str) > 50:
                    repr_str = repr_str[:47] + "..."
                return repr_str

            # Versuche einen sinnvollen String zu finden
            for attr in ['name', 'title', 'description', 'first_name', 'surname', 'email']:
                if hasattr(related_obj, attr):
                    value = getattr(related_obj, attr)
                    if value:
                        return str(value)

            # Fallback: ID
            for attr in ['id', 'p_id', 'pt_id', 'ps_id']:
                if hasattr(related_obj, attr):
                    return f"ID: {getattr(related_obj, attr)}"

            return str(related_obj)
        except Exception as e:
            print(f"Fehler beim Holen von Relationship {rel_name}: {e}")
            return None

    def find_foreign_key_column(model, rel_name):
        """Findet den Fremdschlüssel-Spaltennamen für eine Relationship."""
        inspector = inspect(model)
        rel = inspector.relationships.get(rel_name)
        if not rel:
            return None

        # In SQLAlchemy 2.0 verwenden wir local_columns statt foreign_keys
        # local_columns sind die Spalten im aktuellen Modell, die auf das andere Modell zeigen
        if hasattr(rel, 'local_columns'):
            for column in rel.local_columns:
                return column.name

        # Fallback: Versuche, die Spalte durch Namenskonvention zu finden
        # z.B. relationship "ps_staff" könnte "ps_id" als Fremdschlüssel haben
        possible_fk_names = [
            f"{rel_name}_id",
            f"{rel_name.split('_')[-1]}_id",  # z.B. "staff_id" für "ps_staff"
            rel_name.replace('_staff', '_id'),  # für "ps_staff" -> "ps_id"
            rel_name.replace('_', '') + '_id',  # für "ps_staff" -> "psstaff_id"
        ]

        for column in model.__table__.columns:
            if column.name in possible_fk_names:
                return column.name

        return None

    def to_dict(model_instance, excluded_columns, include_relationships=True):
        """Konvertiert ein Modell-Instanz zu einem Dictionary."""
        excluded_columns = excluded_columns or []
        result = {}

        # Zuerst alle Spalten sammeln
        for column in model_instance.__table__.columns:
            if column.name not in excluded_columns:
                result[column.name] = getattr(model_instance, column.name)

        # Relationships (optional)
        if include_relationships:
            inspector = inspect(model_instance.__class__)
            for rel_name, rel_prop in inspector.relationships.items():
                if rel_name not in excluded_columns:
                    value = get_relationship_value(model_instance, rel_name)
                    if value is not None:
                        # Collections als "Anzahl" kennzeichnen
                        if rel_prop.uselist:
                            result[f"{rel_name}_count"] = value
                        else:
                            result[rel_name] = value
                            # Entferne den Fremdschlüssel aus dem Ergebnis, wenn wir die Relationship anzeigen
                            fk_column = find_foreign_key_column(model_instance.__class__, rel_name)
                            if fk_column and fk_column in result:
                                # Füge FK zur excluded_columns Liste hinzu
                                if fk_column not in excluded_columns:
                                    excluded_columns.append(fk_column)

        return result

    def buildLayout(model, excluded_columns, search_value=None):
        """Erstellt Tabellenlayout für ein Modell."""
        items = load_data(model, search_value)

        if not items:
            # Leere Tabelle mit verfügbaren Spalten
            all_columns = [
                {'name': col.name, 'label': col.name.replace('_', ' ').title(), 'field': col.name}
                for col in model.__table__.columns
                if col.name not in excluded_columns
            ]
            # Relationships hinzufügen, aber ohne Fremdschlüssel-Spalten
            inspector = inspect(model)
            for rel_name, rel_prop in inspector.relationships.items():
                if rel_name not in excluded_columns:
                    if rel_prop.uselist:
                        all_columns.append({
                            'name': f"{rel_name}_count",
                            'label': f"{rel_name.replace('_', ' ').title()} (Anzahl)",
                            'field': f"{rel_name}_count"
                        })
                    else:
                        all_columns.append({
                            'name': rel_name,
                            'label': rel_name.replace('_', ' ').title(),
                            'field': rel_name
                        })

            return [], all_columns

        # Erste Zeile für Spaltendefinition
        first_item_dict = to_dict(items[0], excluded_columns.copy(), include_relationships=True)

        columns = []
        for key in first_item_dict.keys():
            column_def = {
                'name': key,
                'label': key.replace('_', ' ').title(),
                'field': key,
                'sortable': True
            }

            # Besondere Formatierung für bestimmte Spaltentypen
            if key.endswith('_count'):
                column_def['label'] = column_def['label'].replace(' Count', ' (Anzahl)')

            columns.append(column_def)

        # Alle Daten konvertieren
        rows = [to_dict(item, excluded_columns.copy(), include_relationships=True) for item in items]

        return rows, columns

    def build_content():
        print("build_content wird aufgerufen")

        # State-Objekte
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

        def update_table():
            """Aktualisiert die Tabelle basierend auf aktuellen Einstellungen."""
            if not state['current_model']:
                return

            try:
                rows, cols = buildLayout(
                    state['current_model'],
                    state['excluded_columns'],
                    state['search_value']
                )

                # Alte Tabelle entfernen, wenn sie existiert
                if state['table']:
                    try:
                        state['table'].clear()
                        state['table'].delete()
                    except:
                        pass

                # Leere den Tabellen-Container
                if state['table_container']:
                    state['table_container'].clear()

                # Neue Tabelle erstellen, wenn es Daten gibt
                if rows:
                    # Primärschlüssel für row_key finden
                    pk_columns = state['current_model'].__table__.primary_key.columns
                    row_key = list(pk_columns)[0].name if pk_columns else 'id'

                    with state['table_container']:
                        state['table'] = ui.table(
                            rows=rows,
                            columns=cols,
                            row_key=row_key,
                            pagination={'rowsPerPage': 20, 'sortBy': row_key}
                        ).classes('w-full shadow-sm')
                else:
                    with state['table_container']:
                        ui.label("Keine Daten gefunden").classes("text-lg text-gray-500 mt-4")

            except Exception as e:
                ui.notify(f"Fehler beim Aktualisieren der Tabelle: {str(e)}", type='negative')
                print(f"Fehler: {e}")

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

            # Spalten-Checkboxes neu erstellen
            update_column_checkboxes()

            # Tabelle aktualisieren
            update_table()

            ui.notify(f"Modell gewechselt zu: {model_class.__name__}")

        def handle_checkbox_change(column_name, value):
            """Handler für Checkbox-Änderungen."""
            if not value and column_name not in state['excluded_columns']:
                state['excluded_columns'].append(column_name)
            elif value and column_name in state['excluded_columns']:
                state['excluded_columns'].remove(column_name)
            update_table()

        def handle_search_change(suche):
            """Handler für Suchfeld-Änderungen."""
            state['search_value'] = suche.value if suche.value else None
            update_table()

        def update_column_checkboxes():
            """Aktualisiert die Checkboxen für Spaltenauswahl."""
            if not state['current_model']:
                return

            # Alte Checkboxen löschen
            for checkbox in state['column_checkboxes'].values():
                try:
                    checkbox.delete()
                except:
                    pass
            state['column_checkboxes'].clear()

            # Neue Checkboxen erstellen
            if 'column_dropdown_content' in state:
                state['column_dropdown_content'].clear()

                with state['column_dropdown_content']:
                    ui.label("Spalten anzeigen").classes("font-bold mb-3 text-primary")

                    # Normale Spalten (ohme Fremdschlüssel, die durch Relationships abgedeckt werden)
                    for column in state['current_model'].__table__.columns:
                        column_name = column.name
                        # Prüfe, ob diese Spalte ein Fremdschlüssel ist, der durch eine Relationship ersetzt wird
                        is_fk_for_relationship = False
                        inspector = inspect(state['current_model'])
                        for rel_name, rel_prop in inspector.relationships.items():
                            if not rel_prop.uselist:  # Nur Many-to-One/One-to-One
                                fk_column = find_foreign_key_column(state['current_model'], rel_name)
                                if fk_column == column_name:
                                    is_fk_for_relationship = True
                                    break

                        # Zeige nur Checkboxen für Spalten an, die nicht durch Relationships ersetzt werden
                        if not is_fk_for_relationship:
                            # Für Spalten mit "_id": Standardmäßig unchecked, sonst geprüft
                            default_checked = column_name not in state['excluded_columns']

                            cb = ui.checkbox(
                                column_name.replace('_', ' ').title(),
                                value=default_checked,
                                on_change=lambda e, col=column_name: handle_checkbox_change(col, e.value)
                            ).classes("w-full")
                            state['column_checkboxes'][column_name] = cb

                    ui.separator().classes("my-2")
                    ui.label("Beziehungen").classes("font-bold mb-3 text-primary")

                    # Relationships
                    inspector = inspect(state['current_model'])
                    for rel_name, rel_prop in inspector.relationships.items():
                        # Wenn es eine Many-to-One/One-to-One Relationship ist, überspringen wir sie,
                        # da die Fremdschlüssel-Spalte bereits ausgeblendet wurde
                        if not rel_prop.uselist:
                            fk_column = find_foreign_key_column(state['current_model'], rel_name)
                            if fk_column:
                                # Diese Relationship ersetzt eine FK-Spalte, also keine separate Checkbox anzeigen
                                continue

                        label = rel_name.replace('_', ' ').title()
                        if rel_prop.uselist:
                            label = f"{label} (Anzahl)"

                        cb = ui.checkbox(
                            label,
                            value=rel_name not in state['excluded_columns'],
                            on_change=lambda e, col=rel_name: handle_checkbox_change(col, e.value)
                        ).classes("w-full")
                        state['column_checkboxes'][rel_name] = cb

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
                        on_change=lambda e: handle_search_change(e)
                    ).props("dense outlined clearable").classes("w-64")

                    # Settings Dropdown für Spalten
                    with ui.dropdown_button(icon="settings", color="primary").props("flat round dense"):
                        with ui.card().classes("p-4 w-64 max-h-96 overflow-y-auto") as dropdown_content:
                            state['column_dropdown_content'] = dropdown_content
                            update_column_checkboxes()

            # Tabellen-Container (wird bei jedem Update geleert)
            state['table_container'] = ui.column().classes("w-full")

        # Initiale Tabelle erstellen
        if state['current_model']:
            # Zuerst column_checkboxes aufbauen, dann Tabelle
            update_column_checkboxes()
            update_table()
        else:
            with state['table_container']:
                ui.label("Kein Modell ausgewählt").classes("text-lg text-gray-500")

    app_layout(build_content)