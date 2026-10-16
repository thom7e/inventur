#!/bin/sh
# Tägliches Backup der SQLite-DBs, 30 Tage Aufbewahrung
set -e
APP="$HOME/inventur_verbesserung"
DEST="$HOME/inventur_backups"
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p "$DEST"
for db in artikel.db kostenstellen_db.db; do
    python3 -c "
import sqlite3,sys
src=sqlite3.connect('$APP/$db'); dst=sqlite3.connect('$DEST/${db%.db}-$TS.db')
src.backup(dst); dst.close(); src.close()"
done
find "$DEST" -name '*.db' -mtime +30 -delete
