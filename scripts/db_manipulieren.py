#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

# ========= Konfiguration =========
DB_PATH = Path("kostenstellen_db.db")          # Pfad zu deiner *Kostenstellen*-DB
TABLE   = "inventur"                            # Inventur-Tabelle
OCT_FROM = "2025-10-01"
OCT_TO   = "2025-10-31"
# Wenn du die Datumsspalte kennst, kannst du sie hier fest eintragen (überschreibt Auto-Detect):
FORCE_DATE_COL = None  # z.B. "created_at" oder None lassen

# ========= Helfer =========
CANDIDATE_DATE_COLS = ["datum", "date", "created_at", "created", "zeitpunkt", "erfasst_am", "erfasst"]

def backup_db(db_path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = db_path.with_suffix(db_path.suffix + f".bak-{ts}")
    shutil.copy2(db_path, backup)
    return backup

def get_columns(conn, table):
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    # rows: cid, name, type, notnull, dflt_value, pk
    return [r[1] for r in rows]

def detect_date_col(conn, table):
    cols = get_columns(conn, table)
    if FORCE_DATE_COL and FORCE_DATE_COL in cols:
        return FORCE_DATE_COL
    for c in CANDIDATE_DATE_COLS:
        if c in cols:
            return c
    return None

def fetch_count_by_year(conn, table):
    try:
        rows = conn.execute(f"SELECT jahr, COUNT(*) FROM {table} GROUP BY jahr ORDER BY jahr").fetchall()
        return {int(r[0]): int(r[1]) for r in rows if r[0] is not None}
    except Exception:
        return {}

def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB nicht gefunden: {DB_PATH.resolve()}")

    print(f"Arbeite auf DB: {DB_PATH.resolve()}")
    print("Erstelle Backup...")
    backup = backup_db(DB_PATH)
    print(f"Backup erstellt: {backup.name}")

    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.isolation_level = "EXCLUSIVE"
        conn.row_factory = sqlite3.Row

        # Vorher-Statistik
        before = fetch_count_by_year(conn, TABLE)
        print("Zähler vorab (jahr -> count):", before or "(keine Daten/keine jahr-Spalte)")

        # Datumsspalte finden
        date_col = detect_date_col(conn, TABLE)
        if date_col:
            print(f"Gefundene Datumsspalte: {date_col} – lösche Oktober 2025…")
            # DATE() normalisiert 'YYYY-MM-DD HH:MM:SS' auf Datum; bei reinem 'YYYY-MM-DD' unverändert
            delete_sql = f"DELETE FROM {TABLE} WHERE DATE({date_col}) BETWEEN ? AND ?"
            conn.execute("BEGIN")
            cur = conn.execute(delete_sql, (OCT_FROM, OCT_TO))
            deleted = cur.rowcount if hasattr(cur, "rowcount") else None
            conn.commit()
            print(f"…{deleted if deleted is not None else '?'} Zeilen gelöscht (Okt 2025).")
        else:
            print("Keine Datumsspalte gefunden – Überspringe gezieltes Löschen für Oktober 2025.")

        # Jahr von 2025 -> 2024 korrigieren
        print("Setze jahr=2024 für alle verbleibenden Zeilen mit jahr=2025…")
        conn.execute("BEGIN")
        cur = conn.execute(f"UPDATE {TABLE} SET jahr = 2024 WHERE jahr = 2025")
        updated = cur.rowcount if hasattr(cur, "rowcount") else None
        conn.commit()
        print(f"…{updated if updated is not None else '?'} Zeilen aktualisiert.")

        # Nachher-Statistik
        after = fetch_count_by_year(conn, TABLE)
        print("Zähler danach (jahr -> count):", after or "(keine Daten/keine jahr-Spalte)")

    print("Fertig.")

if __name__ == "__main__":
    main()
