import sqlite3
from pathlib import Path

DB = Path("kostenstellen_db.db")

with sqlite3.connect(DB) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute(
        "INSERT OR REPLACE INTO app_meta (key, value) VALUES ('active_inventur_year', ?)",
        ("2025",)
    )
    conn.commit()

print("active_inventur_year -> 2025 gesetzt in", DB.resolve())
