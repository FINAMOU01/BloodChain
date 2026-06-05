FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY services/frontend-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend service code
COPY services/frontend-service/config ./config
COPY services/frontend-service/core ./core
COPY services/frontend-service/manage.py .

# Copy templates and static files from root
COPY templates ./templates
COPY static ./static

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN groupadd -r bloodchain && useradd -r -g bloodchain bloodchain

# Change ownership of app directory
RUN chown -R bloodchain:bloodchain /app

# Switch to non-root user
USER bloodchain

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
