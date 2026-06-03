#!/bin/sh
set -e

echo "Starting BloodChain Rewards Service..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true
echo "Static files collected."

# Start Gunicorn
echo "Starting Gunicorn server..."
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
