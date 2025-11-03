import sqlite3
import pandas as pd
import re


def create_tables(conn):
    cur = conn.cursor()

    # Erstellen der Kostenstellen-Tabelle mit zusätzlichen Spalten
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kostenstellen (
            id INTEGER PRIMARY KEY,
            kostenstellen_nummer TEXT UNIQUE NOT NULL,
            kostenstellen_bezeichnung TEXT NOT NULL
        );
    """)

    # Erstellen der Inventur-Tabelle
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventur (
            id INTEGER PRIMARY KEY,
            kostenstelle TEXT NOT NULL,
            jahr INTEGER NOT NULL,
            artikelname TEXT,
            einheit TEXT,
            menge REAL,
            preis REAL,
            gesamtpreis REAL,
            FOREIGN KEY (kostenstelle) REFERENCES kostenstellen(kostenstellen_nummer)
        );
    """)

    conn.commit()
    cur.close()


def import_kostenstellen_from_excel(conn, file_path):
    df = pd.read_excel(file_path)
    first_column = df.columns[0]  # Erste Spalte der Excel-Datei

    # Extrahierung von Nummer und Bezeichnung der Kostenstellen
    def extract_kostenstelle(cell):
        nummer = re.search(r"\(\s*(\d+)\s*\)", cell)
        bezeichnung = re.sub(r"\(\s*\d+\s*\)", "", cell).strip()
        return nummer.group(1) if nummer else None, bezeichnung

    df[['kostenstellen_nummer', 'kostenstellen_bezeichnung']] = df.apply(
        lambda row: extract_kostenstelle(row[first_column]), axis=1, result_type='expand')

    cur = conn.cursor()
    for _, row in df.iterrows():
        if row['kostenstellen_nummer']:
            cur.execute(
                "INSERT INTO kostenstellen (kostenstellen_nummer, kostenstellen_bezeichnung) VALUES (?, ?) ON CONFLICT (kostenstellen_nummer) DO NOTHING;",
                (row['kostenstellen_nummer'], row['kostenstellen_bezeichnung']))

    conn.commit()
    cur.close()


# Datenbankverbindung
conn = sqlite3.connect('meine_datenbank.db')

create_tables(conn)
import_kostenstellen_from_excel(conn, "kostenstellen.xlsx")

print("Datenbank eingerichtet und Kostenstellen importiert.")
conn.close()
