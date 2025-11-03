import sqlite3


def delete_articles_by_kostenstelle(kostenstelle):
    """
    Löscht alle Artikel aus der Tabelle 'inventur' für eine bestimmte Kostenstelle in der Datenbank 'kostenstellen_db.db'.

    :param kostenstelle: Die Nummer der Kostenstelle, deren Artikel gelöscht werden sollen.
    """
    database = "kostenstellen_db.db"  # SQLite-Datenbank
    table_name = "inventur"  # Tabellenname

    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # SQL-Delete-Befehl ausführen
        query = f"DELETE FROM {table_name} WHERE kostenstelle = ?"
        cursor.execute(query, (kostenstelle,))

        # Änderungen speichern
        conn.commit()
        print(f"Alle Artikel der Kostenstelle mit Nummer '{kostenstelle}' wurden gelöscht.")
    except sqlite3.Error as e:
        print(f"Fehler: {e}")
    finally:
        # Verbindung schließen
        if conn:
            conn.close()


if __name__ == "__main__":
    # Benutzer nach der Kostenstellennummer fragen
    try:
        kostenstelle = (
            input("Bitte geben Sie die Kostenstellennummer ein, deren Artikel gelöscht werden sollen: "))
        confirm = input(
            f"Sind Sie sicher, dass Sie alle Artikel der Kostenstelle '{kostenstelle}' löschen möchten? (ja/nein): ").strip().lower()

        if confirm == "ja":
            delete_articles_by_kostenstelle(kostenstelle)
        else:
            print("Vorgang abgebrochen.")
    except ValueError:
        print("Bitte geben Sie eine gültige Zahl für die Kostenstellennummer ein.")
