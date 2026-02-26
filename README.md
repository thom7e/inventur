# Inventur & Kostenstellen

Eine Flask-Webapp zur Verwaltung von Artikelstämmen, Inventuren und Kostenstellen mit SQLite-Speicher und Excel-Export.

## Features

- **Artikel-Suche & Warenkorb** – Artikel suchen, Mengen erfassen, in die Inventur übernehmen
- **Übersicht Inventur** – Gefilterte Ansicht nach Jahr und Kostenstelle, inline Bearbeiten/Löschen
- **Excel-Export** – Kompletter oder gefilterter Export als `.xlsx`
- **Admin-Bereich** (Login erforderlich)
  - Kostenstellen einzeln oder per Bulk-Import pflegen
  - Artikel verwalten (hinzufügen, bearbeiten, löschen)
  - Preise faktorweise anpassen
  - Jahresabschluss mit Archivierung alter Inventurdaten
- **Sicherheit**
  - CSRF-Schutz auf allen zustandsändernden Endpunkten
  - Admin-Decorator mit JSON/HTML-Response-Unterscheidung
  - Audit-Log (SQLite) für alle kritischen Aktionen
  - Passwort-Hashing via `werkzeug.security`
- **UI/UX**
  - Bootstrap 4 – vollständig responsive
  - Bootstrap-Modals statt `window.prompt/confirm`
  - Loading-Spinner auf allen Async-Buttons
  - Barrierefreiheit: Skip-Link, `aria-current`, `aria-live`, `:focus-visible`

## Projektstruktur

```
inventur/
├── app.py                  # Flask-Anwendung (Routen, Logik, DB-Hilfen)
├── requirements.txt
├── static/
│   └── styles.css          # Eigenes Stylesheet (ergänzt Bootstrap)
├── templates/
│   ├── base.html           # Layout, Navigation, Toast-Benachrichtigungen
│   ├── login.html          # Admin-Login
│   ├── index.html          # Artikel-Suche & Warenkorb
│   ├── admin.html          # Verwaltungsbereich
│   └── uebersicht_inventur.html  # Inventur-Übersicht & Export
└── scripts/                # Optionale Hilfsskripte (pandas-basiert)
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Umgebungsvariablen (optional)

| Variable | Standard | Beschreibung |
|---|---|---|
| `ADMIN_USERNAME` | `admin` | Admin-Benutzername |
| `ADMIN_PASSWORD` | `admin` | Klartext-Passwort (wird beim Start gehasht) |
| `ADMIN_PASSWORD_HASH` | – | Bcrypt-Hash; überschreibt `ADMIN_PASSWORD` |
| `ARTICLE_DB_PATH` | `artikel.db` | Pfad zur Artikel-Datenbank |
| `COST_CENTER_DB_PATH` | `kostenstellen_db.db` | Pfad zur Kostenstellen-/Inventur-Datenbank |
| `SECRET_KEY` | zufällig | Flask Session Secret (für Produktion setzen!) |
| `FLASK_ENV` | `production` | `development` aktiviert Auto-Reload |

### Starten

```bash
python app.py
# oder:
flask --app app run --host 0.0.0.0 --port 5000
```

Die App ist dann unter `http://localhost:5000` erreichbar.
Admin-Login: `http://localhost:5000/login`

## Produktion

Für den Produktiveinsatz unbedingt beachten:

1. `SECRET_KEY` als langen, zufälligen Wert setzen:
   ```bash
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```
2. `ADMIN_PASSWORD` durch einen sicheren Wert ersetzen oder `ADMIN_PASSWORD_HASH` direkt setzen.
3. Einen WSGI-Server verwenden (z. B. `gunicorn`):
   ```bash
   pip install gunicorn
   gunicorn -w 2 -b 0.0.0.0:5000 app:app
   ```
4. HTTPS über einen Reverse-Proxy (nginx/caddy) terminieren.

## Abhängigkeiten

| Paket | Version | Zweck |
|---|---|---|
| Flask | ≥ 3.0 | Web-Framework |
| openpyxl | ≥ 3.1 | Excel-Export |
| pandas | ≥ 2.2 | Hilfsskripte (`scripts/`) |
