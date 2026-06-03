FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --default-timeout=100 --retries=5 -r requirements.txt

# ── Runtime stage ──
FROM python:3.11-slim

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r bloodchain && useradd -r -g bloodchain bloodchain

WORKDIR /app

# Copy Python dependencies from builder
COPY --chown=bloodchain:bloodchain --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings

# Copy entrypoint first and make executable (for manual use)
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN dos2unix /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy application code
COPY --chown=bloodchain:bloodchain . .

# Create staticfiles directory and ensure proper permissions
RUN mkdir -p /app/staticfiles && \
    chown -R bloodchain:bloodchain /app && \
    chmod +x /app/docker-entrypoint.sh

# Switch to non-root user
USER bloodchain

# Proper healthcheck using curl (now installed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

# Run startup script with bash explicitly
CMD ["/bin/bash", "/app/docker-entrypoint.sh"]
