import sqlite3

def update_prices():
    """
    Reduziert alle Preise in der SQLite-Tabelle 'artikel' der Datenbank 'artikel.db' um 1,9 %.
    """
    database = "artikel.db"  # SQLite-Datenbank
    table_name = "artikel"   # Tabellenname
    price_column = "preis"   # Preisspalte
    discount_percentage = 1.9  # Prozentuale Reduktion

    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        # Reduzierungsfaktor berechnen
        factor = 1 - (discount_percentage / 100)
        
        # SQL-Update-Befehl ausführen
        query = f"UPDATE {table_name} SET {price_column} = {price_column} * ?"
        cursor.execute(query, (factor,))
        
        # Änderungen speichern
        conn.commit()
        print(f"Alle Preise in der Tabelle '{table_name}' in der Datenbank '{database}' wurden um {discount_percentage}% reduziert.")
    except sqlite3.Error as e:
        print(f"Fehler: {e}")
    finally:
        # Verbindung schließen
        if conn:
            conn.close()

# Skript ausführen
if __name__ == "__main__":
    update_prices()
