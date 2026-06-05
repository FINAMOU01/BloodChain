FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a proper Python virtual environment with symlinks
RUN python -m venv /opt/venv && \
    ln -sf /usr/local/bin/python3 /opt/venv/bin/python && \
    ln -sf /usr/local/bin/python3 /opt/venv/bin/python3

ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --default-timeout=300 --retries=5 -r requirements.txt

# ── Runtime stage ──
FROM python:3.11-slim

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r bloodchain && useradd -r -g bloodchain bloodchain

WORKDIR /app

# Copy Python dependencies from builder and fix permissions
COPY --from=builder --chown=bloodchain:bloodchain /opt/venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings

# Copy entrypoint first and make executable
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy application code
COPY --chown=bloodchain:bloodchain . .

# Create staticfiles directory
RUN mkdir -p /app/staticfiles && \
    chown bloodchain:bloodchain /app && \
    chown -R bloodchain:bloodchain /app/staticfiles

# Switch to non-root user
USER bloodchain

# Proper healthcheck using curl (now installed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
