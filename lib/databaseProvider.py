import sqlite3
import os


class DatabaseProvider:
    _instance = None
    _connection = None
    _db_path = "Database.db"


    """Digga python singletons sind weird aber geil
    cls ist das keyword für klasseneigene variablen. 
    self. bezieht sich auf die Instanz der Klasse, cls. auf die klasse selbst."""
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseProvider, cls).__new__(cls)
        return cls._instance

    # ------------------- Grundfunktionen -------------------

    def connect(self):
        """Öffnet oder erstellt eine SQLite-Datenbank."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            print(f"✅ Verbindung zur Datenbank '{self._db_path}' hergestellt.")
        return self._connection

    def close(self):
        """Schließt die Verbindung zur Datenbank."""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("🔒 Verbindung geschlossen.")

    def _check_table_exists(self, table_name: str) -> bool:
        """Prüft, ob eine Tabelle bereits existiert."""
        dataBase = self.connect()
        cursor = dataBase.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return cursor.fetchone() is not None

    # ------------------- Setup & Tabellenverwaltung -------------------

    def create_table(self, table_name: str, columns: list[tuple[str, str]], primary_key: str = None):
        """
        Erstellt eine Tabelle mit den angegebenen Spalten.
        columns: Liste von Tupeln (spaltenname, typ)
        Beispiel: [("id", "TEXT"), ("age", "INTEGER"), ("is_active", "BOOLEAN")]
        """
        dataBase = self.connect()

        if self._check_table_exists(table_name):
            print(f"ℹ️ Tabelle '{table_name}' existiert bereits – wird nicht neu erstellt.")
            return

        columns = [(col, typ) for col, typ in columns if col != primary_key]

        col_defs = [f"{col} {typ}" for col, typ in columns]

        if primary_key:
            col_defs.insert(0, f"{primary_key} TEXT PRIMARY KEY")

        sql = f"CREATE TABLE {table_name} ({', '.join(col_defs)})"
        dataBase.execute(sql)
        dataBase.commit()
        print(f"✅ Tabelle '{table_name}' wurde erstellt.")

    def update_table(self, table_name: str, columns: list[tuple[str, str]]):
        """Fügt neue Spalten hinzu, falls sie noch nicht existieren."""
        dataBase = self.connect()
        cursor = dataBase.execute(f"PRAGMA table_info({table_name})")
        existing_cols = [row[1] for row in cursor.fetchall()]

        for col, typ in columns:
            if col not in existing_cols:
                dataBase.execute(f"ALTER TABLE {table_name} ADD COLUMN {col} {typ}")
                print(f"➕ Spalte '{col}' zu '{table_name}' hinzugefügt.")
        dataBase.commit()

    # ------------------- CRUD-Operationen -------------------

    def insert(self, table_name: str, data: dict):
        """Fügt eine Zeile ein. data = { 'name': 'Alice', 'age': 25 }"""
        dataBase = self.connect()
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        values = tuple(data.values())

        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        dataBase.execute(sql, values)
        dataBase.commit()
        print(f"✅ Datensatz in '{table_name}' eingefügt: {data}")

    def update(self, table_name: str, key_col: str, key_val, updates: dict):
        """Aktualisiert Spaltenwerte für eine Zeile."""
        dataBase = self.connect()
        set_clause = ", ".join([f"{k}=?" for k in updates])
        values = list(updates.values()) + [key_val]
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {key_col}=?"
        dataBase.execute(sql, values)
        dataBase.commit()
        print(f"✏️ Datensatz in '{table_name}' aktualisiert: {updates}")

    def delete(self, table_name: str, key_col: str, key_val):
        """Löscht eine Zeile anhand eines Primärschlüssels."""
        dataBase = self.connect()
        sql = f"DELETE FROM {table_name} WHERE {key_col}=?"
        dataBase.execute(sql, (key_val,))
        dataBase.commit()
        print(f"🗑️ Datensatz in '{table_name}' gelöscht, {key_col}={key_val}")

    def select_all(self, table_name: str):
        """Gibt alle Zeilen der Tabelle zurück."""
        dataBase = self.connect()
        cursor = dataBase.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"📋 {len(rows)} Zeilen in '{table_name}':")
        for row in rows:
            print(row)
        return rows

    def select_column(self, table_name: str, column: str):
        """Gibt alle Werte einer Spalte zurück."""
        dataBase = self.connect()
        cursor = dataBase.execute(f"SELECT {column} FROM {table_name}")
        return [row[0] for row in cursor.fetchall()]


# ------------------- Beispielnutzung -------------------

"""if __name__ == "__main__":
    dataBase = DatabaseProvider()

    dataBase.create_table(
        "DiaryCardEntries",
        [("date", "TEXT"), ("mood", "INTEGER"), ("note", "TEXT")],
        primary_key="date"
    )

    dataBase.insert("DiaryCardEntries", {"date": "2025-11-12", "mood": 7, "note": "Guter Tag"})
    dataBase.insert("DiaryCardEntries", {"date": "2025-11-11", "mood": 3, "note": "Etwas stressig"})

    dataBase.select_all("DiaryCardEntries")

    dataBase.update("DiaryCardEntries", "date", "2025-11-12", {"mood": 9})
    dataBase.select_all("DiaryCardEntries")

    dataBase.delete("DiaryCardEntries", "date", "2025-11-11")
    dataBase.select_all("DiaryCardEntries")"""