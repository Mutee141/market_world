#!/usr/bin/env bash
set -o errexit

echo "=== Importing data from fixtures_store.json ==="
python manage.py loaddata fixtures_store.json

echo "=== Import complete ==="
