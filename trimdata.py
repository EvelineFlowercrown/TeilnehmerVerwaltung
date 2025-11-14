import pandas as pd


def remove_duplicates(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path)

    seen = set()
    unique_rows = []

    for _, row in df.iterrows():
        key = (row[df.columns[0]], row[df.columns[1]])  # erste zwei Spalten
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    # Neue CSV nur mit eindeutigen Zeilen speichern
    unique_df = pd.DataFrame(unique_rows)
    unique_df.to_csv(output_path, index=False)
    print(f"✅ {len(unique_rows)} eindeutige Zeilen gespeichert, {len(df) - len(unique_rows)} Duplikate entfernt.")


# Beispiel verwenden:
remove_duplicates("data/Praktikum.csv", "data/Praktikum.csv")