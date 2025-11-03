import sqlite3


def add_kostenstelle(kostenstellen_nummer, kostenstellen_bezeichnung):
    """
    Fügt eine neue Kostenstelle in die Tabelle 'kostenstellen' der Datenbank 'kostenstellen_db.db' ein.

    :param kostenstellen_nummer: Die Nummer der neuen Kostenstelle
    :param kostenstellen_bezeichnung: Die Bezeichnung der neuen Kostenstelle
    """
    database = "kostenstellen_db.db"  # SQLite-Datenbank
    table_name = "kostenstellen"  # Tabellenname

    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # SQL-Insert-Befehl ausführen
        query = f"INSERT INTO {table_name} (kostenstellen_nummer, kostenstellen_bezeichnung) VALUES (?, ?)"
        cursor.execute(query, (kostenstellen_nummer, kostenstellen_bezeichnung))

        # Änderungen speichern
        conn.commit()
        print(f"Kostenstelle '{kostenstellen_bezeichnung}' mit Nummer '{kostenstellen_nummer}' wurde hinzugefügt.")
    except sqlite3.Error as e:
        print(f"Fehler: {e}")
    finally:
        # Verbindung schließen
        if conn:
            conn.close()


if __name__ == "__main__":
    # Benutzer nach den Werten fragen
    try:
        kostenstellen_nummer = int(input("Bitte geben Sie die Kostenstellennummer ein: "))
        kostenstellen_bezeichnung = input("Bitte geben Sie die Kostenstellenbezeichnung ein: ").strip()

        if not kostenstellen_bezeichnung:
            print("Die Kostenstellenbezeichnung darf nicht leer sein!")
        else:
            add_kostenstelle(kostenstellen_nummer, kostenstellen_bezeichnung)
    except ValueError:
        print("Bitte geben Sie eine gültige Zahl für die Kostenstellennummer ein.")
