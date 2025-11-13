import os
import sqlite3
import pytest
from lib.databaseProvider import DatabaseProvider


@pytest.fixture
def db(tmp_path):
    """Erstellt eine temporäre Datenbank für Tests."""
    db_path = tmp_path / "test.db"
    provider = DatabaseProvider()
    provider._db_path = str(db_path)  # überschreibe Pfad
    provider._connection = None       # erzwinge neue Verbindung
    yield provider
    provider.close()
    if os.path.exists(db_path):
        os.remove(db_path)


def test_singleton_behavior():
    """
    - Testet, dass DatabaseProvider ein Singleton ist.
    - Wir erstellen 2 databaseprovider und schauen ob sie auf das gleiche Objekt verweisen
    """
    db1 = DatabaseProvider()
    db2 = DatabaseProvider()
    assert db1 is db2, "DatabaseProvider sollte ein Singleton sein"

    """
    - Testet, ob die Datenbank geöffnet und wieder geschlossen werden kann
    """
def test_connect_and_close(db):
    conn = db.connect()
    assert isinstance(conn, sqlite3.Connection)
    db.close()
    assert db._connection is None

    """
    - Testet, ob tabellen korrekt erstellt werden
    """
def test_create_table_and_check_exists(db):
    db.create_table("TestTable", [("id", "INTEGER"), ("name", "TEXT")], primary_key="id")
    assert db._check_table_exists("TestTable")

    # erneutes Erstellen sollte keine Exception werfen
    db.create_table("TestTable", [("id", "INTEGER"), ("name", "TEXT")], primary_key="id")


def test_insert_and_select_all(db):
    db.create_table("People", [("id", "TEXT"), ("name", "TEXT")], primary_key="id")

    db.insert("People", {"id": "1", "name": "Alice"})
    db.insert("People", {"id": "2", "name": "Bob"})

    rows = db.select_all("People")
    assert len(rows) == 2
    assert rows[0][1] == "Alice"
    assert rows[1][1] == "Bob"


def test_select_column(db):
    db.create_table("Items", [("id", "TEXT"), ("price", "INTEGER")], primary_key="id")
    db.insert("Items", {"id": "a", "price": 100})
    db.insert("Items", {"id": "b", "price": 200})

    prices = db.select_column("Items", "price")
    assert prices == [100, 200]


def test_update(db):
    db.create_table("Diary", [("date", "TEXT"), ("mood", "INTEGER")], primary_key="date")
    db.insert("Diary", {"date": "2025-11-12", "mood": 5})

    db.update("Diary", "date", "2025-11-12", {"mood": 9})

    rows = db.select_all("Diary")
    assert rows[0][1] == 9


def test_delete(db):
    db.create_table("Temp", [("id", "TEXT"), ("val", "INTEGER")], primary_key="id")
    db.insert("Temp", {"id": "x", "val": 10})
    db.delete("Temp", "id", "x")

    rows = db.select_all("Temp")
    assert rows == []


def test_update_table_add_column(db):
    db.create_table("Config", [("id", "TEXT")], primary_key="id")
    db.update_table("Config", [("version", "INTEGER"), ("active", "BOOLEAN")])

    cols = [row[1] for row in db.connect().execute("PRAGMA table_info(Config)").fetchall()]
    assert "version" in cols
    assert "active" in cols
