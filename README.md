# Inventur & Kostenstellen

Eine webbasierte Inventurverwaltung auf Basis von **Python / Flask** und **SQLite**. Erfassung von Artikeln nach Kostenstelle und Jahr, Preispflege, Jahresabschluss und Excel-Export – alles ohne externe Datenbank.

---

## Inhaltsverzeichnis

- [Features](#features)
- [Screenshots / Seitenübersicht](#seitenübersicht)
- [Projektstruktur](#projektstruktur)
- [Quickstart](#quickstart)
- [Konfiguration](#konfiguration)
- [Routen-Übersicht](#routen-übersicht)
- [Datenbankschema](#datenbankschema)
- [Sicherheit](#sicherheit)
- [Excel-Export](#excel-export)
- [Hilfsskripte](#hilfsskripte)
- [Produktion](#produktion)
- [Abhängigkeiten](#abhängigkeiten)

---

## Features

### Für alle Nutzer
| Feature | Beschreibung |
|---|---|
| **Artikelsuche** | Volltextsuche ab 2 Zeichen mit Debounce, noscript-Fallback |
| **Warenkorb** | Serverseitiger Warenkorb (SQLite, session-gebunden), Mengen editierbar |
| **Inventur speichern** | Warenkorb mit Bestätigungs-Modal in Inventur übernehmen |
| **Inventur-Übersicht** | Gefiltert nach Jahr und Kostenstelle, Summen je Kostenstelle |
| **Bearbeiten / Löschen** | Einzelne Inventurzeilen inline bearbeiten oder löschen (aktives Jahr) |
| **Excel-Export** | Gesamtexport oder gefilterter Export nach Jahr / Kostenstelle |

### Admin-Bereich (Login erforderlich)
| Feature | Beschreibung |
|---|---|
| **Artikelstamm** | Artikel hinzufügen, bearbeiten, löschen |
| **Kostenstellen** | Einzeln oder per Bulk-Import (mehrzeiliges Textarea) pflegen |
| **Kostenstellen leeren** | Alle Kostenstellen auf einmal entfernen (mit Bestätigungs-Modal) |
| **Preisfaktor** | Alle Artikelpreise prozentual anpassen (z. B. +5 %) |
| **Jahresabschluss** | Aktive Kostenstellen archivieren, neue Jahresliste einlesen |
| **Audit-Log** | Alle kritischen Aktionen werden in SQLite protokolliert |

---

## Seitenübersicht

| URL | Seite | Zugang |
|---|---|---|
| `/` | Artikelsuche & Warenkorb | Öffentlich |
| `/uebersicht_inventur` | Inventurübersicht & Export | Öffentlich |
| `/login` | Admin-Login | Öffentlich |
| `/admin` | Verwaltungsbereich | Admin |
| `/logout` | Abmelden | Admin |

---

## Projektstruktur

```
inventur/
├── app.py                        # Flask-App: Routen, Logik, DB-Hilfsfunktionen
├── requirements.txt              # Python-Abhängigkeiten
├── CHANGELOG.md                  # Versionshistorie
│
├── static/
│   └── styles.css                # Eigenes Stylesheet (ergänzt Bootstrap 4)
│
├── templates/
│   ├── base.html                 # Layout, Navigation, Toast-System, Skip-Link
│   ├── login.html                # Admin-Login-Formular
│   ├── index.html                # Artikelsuche, Warenkorb, Inventur speichern
│   ├── admin.html                # Verwaltungsbereich (Artikel, Kostenstellen, Tools)
│   └── uebersicht_inventur.html  # Inventurübersicht, Filter, Export
│
├── scripts/                      # Optionale Hilfsskripte (pandas-basiert, s. u.)
│   ├── db erstellen.py
│   ├── db_manipulieren.py
│   ├── kostenstelle_hinzufuegen.py
│   ├── preis_aendern.py
│   └── update_price.py
│
└── examples/                     # Beispieldaten / Vorlagen
```

---

## Quickstart

### Voraussetzungen
- Python 3.10 oder neuer

### Installation

```bash
# 1. Repo klonen
git clone <repo-url>
cd inventur

# 2. Virtuelle Umgebung erstellen und aktivieren
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. App starten
python app.py
```

Die App ist nun unter **http://localhost:5000** erreichbar.
Admin-Login: **http://localhost:5000/login** (Standard: `admin` / `admin`)

> **Hinweis:** Beim ersten Start werden alle SQLite-Tabellen automatisch angelegt.

---

## Konfiguration

Alle Einstellungen erfolgen über **Umgebungsvariablen**. Es ist keine Konfigurationsdatei erforderlich.

| Variable | Standard | Beschreibung |
|---|---|---|
| `FLASK_SECRET_KEY` | zufällig generiert | Session-Schlüssel. **Für Produktion zwingend setzen!** |
| `ADMIN_USERNAME` | `admin` | Benutzername für den Admin-Bereich |
| `ADMIN_PASSWORD` | `admin` | Klartext-Passwort – wird beim Start gehasht |
| `ADMIN_PASSWORD_HASH` | – | Bereits gehashtes Passwort (überschreibt `ADMIN_PASSWORD`) |
| `ARTICLE_DB_PATH` | `artikel.db` | Pfad zur Artikel-Datenbank |
| `COST_CENTER_DB_PATH` | `kostenstellen_db.db` | Pfad zur Kostenstellen- / Inventur-Datenbank |

### Beispiel `.env` (mit `python-dotenv` oder manuell exportieren)

```bash
export FLASK_SECRET_KEY="ein-langes-zufaelliges-geheimnis"
export ADMIN_USERNAME="inventur"
export ADMIN_PASSWORD="sicheres-passwort"
export ARTICLE_DB_PATH="/data/artikel.db"
export COST_CENTER_DB_PATH="/data/kostenstellen.db"
```

### Passwort-Hash vorab generieren

```bash
python - <<'EOF'
from werkzeug.security import generate_password_hash
print(generate_password_hash("mein-passwort"))
EOF
# Ausgabe als ADMIN_PASSWORD_HASH setzen
```

---

## Routen-Übersicht

### Öffentliche Routen

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/` | Startseite: Artikelsuche & Warenkorb |
| `POST` | `/` | Artikel direkt per Formular suchen (noscript) |
| `POST` | `/search` | AJAX-Artikelsuche (JSON) |
| `GET` | `/get_cart` | Aktuellen Warenkorb abrufen (JSON) |
| `POST` | `/add_to_cart` | Artikel in Warenkorb legen (JSON) |
| `POST` | `/clear_cart` | Warenkorb leeren |
| `POST` | `/export_excel` | Warenkorb als Excel exportieren |
| `POST` | `/save_to_inventur` | Warenkorb in Inventur speichern |
| `GET` | `/uebersicht_inventur` | Inventurübersicht (optional `?jahr=YYYY`) |
| `POST` | `/export_inventur` | Kompletten Inventurexport herunterladen |
| `POST` | `/export_inventur_selection` | Gefilterten Export herunterladen |
| `GET` | `/login` | Login-Seite |
| `POST` | `/login` | Login verarbeiten |
| `GET` | `/logout` | Abmelden |

### Admin-Routen (Login + CSRF erforderlich)

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/admin` | Verwaltungsübersicht |
| `POST` | `/admin/search` | Admin-Artikelsuche (JSON) |
| `POST` | `/add_artikel` | Artikel zu Warenkorb hinzufügen (Admin-Suche) |
| `POST` | `/add_article` | Neuen Artikel im Stamm anlegen |
| `POST` | `/update_article` | Artikel bearbeiten |
| `POST` | `/delete_article` | Artikel löschen |
| `POST` | `/admin/add_cost_center` | Einzelne Kostenstelle hinzufügen |
| `POST` | `/admin/bulk_add_cost_centers` | Kostenstellen per Bulk-Import hinzufügen |
| `POST` | `/admin/clear_cost_centers` | Alle Kostenstellen löschen |
| `POST` | `/admin/apply_price_factor` | Preisfaktor auf alle Artikel anwenden |
| `POST` | `/admin/year_end` | Jahresabschluss durchführen |
| `POST` | `/admin/inventur/update_row` | Inventurzeile bearbeiten (JSON) |
| `POST` | `/admin/inventur/delete_row` | Inventurzeile löschen (JSON) |

---

## Datenbankschema

Die App verwendet **zwei SQLite-Dateien**:

### `artikel.db` – Artikelstammdaten

```sql
CREATE TABLE artikel (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL UNIQUE,
    einheit   TEXT    NOT NULL,
    preis     REAL    NOT NULL
);
```

### `kostenstellen_db.db` – Kostenstellen, Inventur & Metadaten

```sql
-- Aktive Kostenstellen
CREATE TABLE kostenstellen (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Inventurdaten
CREATE TABLE inventur (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    kostenstelle TEXT    NOT NULL,
    artikelname  TEXT    NOT NULL,
    menge        REAL    NOT NULL,
    einheit      TEXT    NOT NULL,
    preis        REAL    NOT NULL,
    gesamtpreis  REAL    NOT NULL,
    jahr         INTEGER NOT NULL
);

-- Archiv vergangener Kostenstellen (nach Jahresabschluss)
CREATE TABLE kostenstellen_archiv (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    jahr INTEGER NOT NULL
);

-- App-Metadaten (z. B. aktives Inventurjahr)
CREATE TABLE app_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- Serverseitiger Warenkorb
CREATE TABLE cart (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_token   TEXT NOT NULL,
    artikelname  TEXT NOT NULL,
    menge        REAL NOT NULL,
    einheit      TEXT NOT NULL,
    preis        REAL NOT NULL,
    gesamtpreis  REAL NOT NULL
);

-- Audit-Log für Admin-Aktionen
CREATE TABLE audit_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user      TEXT NOT NULL,
    action    TEXT NOT NULL,
    details   TEXT
);
```

---

## Sicherheit

### CSRF-Schutz
Alle zustandsändernden Endpunkte (`POST`, `PUT`, `PATCH`, `DELETE`) sind durch einen session-basierten CSRF-Token geschützt. Der Token wird akzeptiert als:
- Hidden-Field `_csrf_token` in HTML-Formularen
- HTTP-Header `X-CSRF-Token` (AJAX-Requests)
- JSON-Body-Feld `_csrf_token`

### Admin-Authentifizierung
- Passwörter werden mit `werkzeug.security.generate_password_hash` (PBKDF2-HMAC-SHA256) gehasht
- Session-Lebensdauer: 8 Stunden (`PERMANENT_SESSION_LIFETIME`)
- Session-Cookie: `HttpOnly`, `SameSite=Lax`
- Alle Admin-Routen sind mit `@require_admin` dekoriert

### Audit-Log
Folgende Aktionen werden mit Zeitstempel (UTC), Benutzer und Details protokolliert:

| Aktion | Trigger |
|---|---|
| `admin_login` | Erfolgreicher Login |
| `kostenstellen_geleert` | Alle Kostenstellen gelöscht |
| `kostenstelle_hinzugefuegt` | Einzelne Kostenstelle angelegt |
| `kostenstellen_bulk_hinzugefuegt` | Bulk-Import durchgeführt |
| `inventur_zeile_aktualisiert` | Inventurzeile bearbeitet |
| `inventur_zeile_geloescht` | Inventurzeile gelöscht |
| `inventur_gespeichert` | Warenkorb in Inventur übernommen |
| `preisfaktor_angewendet` | Preisfaktor auf Artikel angewendet |
| `jahresabschluss` | Jahresabschluss durchgeführt |
| `artikel_aktualisiert` | Artikel im Stamm geändert |
| `artikel_geloescht` | Artikel aus Stamm entfernt |
| `artikel_hinzugefuegt` | Neuer Artikel im Stamm angelegt |

### Eingabevalidierung
- Dezimalwerte werden über `decimal.Decimal` mit expliziter Komma/Punkt-Normalisierung geparst
- Maximale Feldlängen via `maxlength`-Attribute im Frontend
- Mengen und Preise werden serverseitig auf positive Werte geprüft

---

## Excel-Export

Es gibt drei Export-Varianten:

| Endpunkt | Beschreibung |
|---|---|
| `POST /export_excel` | Aktuellen **Warenkorb** exportieren |
| `POST /export_inventur` | **Gesamte Inventur** exportieren (optional gefiltert nach Jahr) |
| `POST /export_inventur_selection` | **Gefilterte Inventur** nach Jahr und/oder ausgewählten Kostenstellen |

Alle Exporte erzeugen `.xlsx`-Dateien mit:
- Kopfzeilen (fett, Hintergrundfarbe)
- Automatisch angepassten Spaltenbreiten
- Zwischensummen je Kostenstelle
- Gesamtsumme am Ende

---

## Hilfsskripte

Die Skripte unter `scripts/` dienen der einmaligen Datenmigration oder manuellen Datenbankpflege und benötigen `pandas`:

```bash
pip install pandas openpyxl   # falls nicht bereits installiert
```

| Skript | Zweck |
|---|---|
| `db erstellen.py` | Initiale Datenbankstruktur anlegen |
| `db_manipulieren.py` | Direkte Datenbankmanipulation |
| `kostenstelle_hinzufuegen.py` | Kostenstellen per Skript importieren |
| `preis_aendern.py` | Preise per Skript aktualisieren |
| `update_price.py` | Preise aus Excel-Datei einlesen |

> Diese Skripte sind **nicht** für den regulären Betrieb erforderlich.

---

## Produktion

### 1. Secret Key setzen

```bash
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

### 2. Sicheres Admin-Passwort setzen

```bash
export ADMIN_PASSWORD="langes-sicheres-passwort"
# oder direkt mit Hash:
export ADMIN_PASSWORD_HASH=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('passwort'))")
```

### 3. WSGI-Server verwenden

```bash
pip install gunicorn
gunicorn -w 2 -b 127.0.0.1:5000 app:app
```

### 4. Reverse-Proxy (nginx)

```nginx
server {
    listen 443 ssl;
    server_name inventur.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Datenbankdateien sichern

```bash
# Tägliches Backup (Cron)
cp /data/artikel.db /backup/artikel_$(date +%F).db
cp /data/kostenstellen.db /backup/kostenstellen_$(date +%F).db
```

---

## Abhängigkeiten

| Paket | Version | Zweck |
|---|---|---|
| [Flask](https://flask.palletsprojects.com/) | ≥ 3.0 | Web-Framework |
| [Werkzeug](https://werkzeug.palletsprojects.com/) | ≥ 3.0 | Passwort-Hashing (`werkzeug.security`) |
| [openpyxl](https://openpyxl.readthedocs.io/) | ≥ 3.1 | Excel-Export (`.xlsx`) |
| [pandas](https://pandas.pydata.org/) | ≥ 2.2 | Nur für `scripts/` (optional) |

Alle anderen verwendeten Module (`sqlite3`, `decimal`, `secrets`, `logging`, …) sind Teil der Python-Standardbibliothek.
