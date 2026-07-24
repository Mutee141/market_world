#!/usr/bin/env bash
# build.sh — Render build script
set -o errexit

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py migrate --no-input

# Ensure database is clean before loading fixtures
echo "=== Flushing any existing data (if any) ==="
python manage.py flush --no-input

# Load initial data from fixtures_store.json
echo "=== Loading initial data from fixtures_store.json ==="
python manage.py loaddata fixtures_store.json || echo "⚠️ Data load failed - check logs"

echo "=== Build complete ==="
