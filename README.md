# Inventur & Kostenstellen (Flask)

Eine kleine Flask-Webapp zur Verwaltung von Artikeln, Inventur und Kostenstellen mit SQLite und Excel-Export.

## Features
- Suche/Filter von Artikeln (`/search`), Warenkorb und Inventur speichern
- Admin-Bereich mit Login (`/admin`)
  - Kostenstellen einzeln/als Bulk pflegen
  - Preise faktorweise anpassen
  - Jahresabschluss (`/admin/year_end`) mit Archivierung
- Excel-Export (Inventur & Übersicht)
- SQLite als Datenspeicher (lokale Datei)

## Projektstruktur
Siehe Repo-Baum im Root (Templates/Static, optionale `scripts/`, optionale `examples/`).

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Optional) Umgebungsvariablen
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin           # Hash wird beim Start erzeugt, wenn kein ADMIN_PASSWORD_HASH gesetzt ist
export ARTICLE_DB_PATH=artikel.db
export COST_CENTER_DB_PATH=kostenstellen_db.db
export FLASK_ENV=development          # Auto-Reload

# Start
python app.py
# oder:
# flask --app app run --host 0.0.0.0 --port 5000
