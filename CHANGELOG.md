# Changelog

## 2025-10-02
- Config (Secret Key, Admin-Login, Datenbankpfade) wandert in Umgebungsvariablen; Login nutzt Passwort-Hashing.
- Serverseitiger Warenkorb in SQLite mit Validierungen für Mengen und Preise sowie saubere Fehlerantworten.
- Einheitliche DB-Zugriffe über Kontextmanager plus anpassbare Formatierungen für Excel- und Inventurausgaben.
- Neue Basis-Templates mit Toast-Feedback, Debounce-Suche und responsivem Styling.
- Frontend aktualisiert mit besserem Abstandslayout, drei sichtbaren Suchergebnissen im scrollbaren Bereich und konsequent zweistelligen Preisangaben.
- Admin-Tools: Faktor-basierte Preisaktualisierung, Jahresabschluss mit Archivierung der Kostenstellen und Übergabe einer neuen Kostenstellenliste.

- Fix: Javascript-Delegation für Warenkorb-Suche (max drei sichtbare Einträge scrollbar) und robuste Admin-Buttons (Delegation, Null-Schutz).
- Umbau der Suchergebnisse zur DOM-Erzeugung mit sicheren Daten-IDs, damit Sonderzeichen und Anführungszeichen funktionieren.
- Fix: Robust Decimal-Parsing für alle Artikellisten (Such-API/Admin) inklusive Alt-Datensätze mit Komma/Leerzeichen, damit die Suche wieder HTTP 200 liefert.
- Such-Frontend zeigt dank DOM-Aufbau alle Treffer (scrollbar), Admin-Suche filtert wieder clientseitig nach jeder Eingabe.
- UX: Suchformular mit sichtbarer 'Suchen'-Schaltflaeche und serverseitigem Fallback, damit Abfragen auch ohne JavaScript funktionieren.
- Index: automatische Suche ab zwei Zeichen (ohne sichtbaren Button) mit noscript-Fallback und korrekt dargestellten Umlauten.
- Admin: Suchergebnisliste mit Karten (maximal drei sichtbare Einträge, Scrollbereich) + direkter Zugriff auf Bearbeiten/Löschen und UTF-8-Korrekturen.
