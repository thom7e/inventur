import sqlite3

def update_price_interactive():
    """
    Fragt die Kostenstelle, den Artikel und den neuen Preis ab und aktualisiert den Preis in der Tabelle 'inventur'.
    """
    database = "kostenstellen_db.db"  # SQLite-Datenbank
    table_name = "inventur"           # Tabellenname

    try:
        # Benutzer nach Details fragen
        kostenstelle = input("Geben Sie die Kostenstelle ein (z. B. '12318-Hoppe, Illingen'): ").strip()
        artikelname = input("Geben Sie den Artikelnamen ein (z. B. 'Bauholz'): ").strip()
        neuer_preis = float(input("Geben Sie den neuen Preis für den Artikel ein (z. B. 0.7): "))
        
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        # SQL-Update-Befehl ausführen
        query = f"""
        UPDATE {table_name}
        SET preis = ?
        WHERE kostenstelle = ? AND artikelname = ?
        """
        cursor.execute(query, (neuer_preis, kostenstelle, artikelname))
        
        # Änderungen speichern
        conn.commit()
        
        # Überprüfen, ob eine Zeile aktualisiert wurde
        if cursor.rowcount > 0:
            print(f"Der Preis des Artikels '{artikelname}' in der Kostenstelle '{kostenstelle}' wurde auf {neuer_preis} geändert.")
        else:
            print(f"Kein Eintrag gefunden für Artikel '{artikelname}' in der Kostenstelle '{kostenstelle}'.")
    except ValueError:
        print("Ungültige Eingabe! Bitte geben Sie eine gültige Zahl für den Preis ein.")
    except sqlite3.Error as e:
        print(f"Fehler: {e}")
    finally:
        # Verbindung schließen
        if conn:
            conn.close()

if __name__ == "__main__":
    update_price_interactive()
