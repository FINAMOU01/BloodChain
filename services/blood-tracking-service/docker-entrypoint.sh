#!/bin/sh
set -e

# Database connection parameters
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_MAX_RETRIES=120
RETRY_COUNT=0

echo "Starting BloodChain Django service..."

# 1. Wait for database to be ready
echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
while [ $RETRY_COUNT -lt $DB_MAX_RETRIES ]; do
    if python -c "
import psycopg2
import os

try:
    psycopg2.connect(
        host='${DB_HOST}',
        port=${DB_PORT},
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'postgres')
    )
except Exception as e:
    exit(1)
" 2>/dev/null; then
        echo "Database ready!"
        break
    fi
    
    echo "Waiting for database..."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $DB_MAX_RETRIES ]; then
    echo "ERROR: Database did not become ready after 240 seconds"
    exit 1
fi

# 2. Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput
echo "Migrations complete."

# 3. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Static files collected."

# 4. Start Gunicorn
echo "Starting Gunicorn server..."
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
