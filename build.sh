#!/usr/bin/env bash
# build.sh — Render build script
set -o errexit

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py migrate --no-input

echo "=== Checking if store data needs to be loaded ==="
STORE_COUNT=$(python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from tenants.models import Store
print(Store.objects.count())
" 2>/dev/null || echo "0")

if [ "$STORE_COUNT" = "0" ]; then
    echo "=== No store found — loading existing data from fixtures_store.json ==="
    python manage.py loaddata fixtures_store.json
    echo "=== Data loaded successfully! ==="
else
    echo "=== Store already exists (count: $STORE_COUNT) — skipping data load ==="
fi

echo "=== Build complete ==="
