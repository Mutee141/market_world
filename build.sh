#!/usr/bin/env bash
# build.sh — Render build script
set -o errexit

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py migrate --no-input

# Load initial data from fixtures_store.json if required
echo "=== Loading data from fixtures_store.json ==="
python manage.py loaddata fixtures_store.json || echo "⚠️ Data load note: existing data preserved or duplicate keys skipped"

echo "=== Ensuring live Admin account exists ==="
python manage.py ensure_admin

echo "=== Build complete ==="


