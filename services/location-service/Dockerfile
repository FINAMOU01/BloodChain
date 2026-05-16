FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies for GDAL and PostGIS
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ── Runtime stage ──
FROM python:3.11-slim

# Install runtime dependencies for GDAL and PostGIS
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r bloodchain && useradd -r -g bloodchain bloodchain

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make gunicorn and other executables readable/executable by non-root user
RUN chmod -R a+rx /root/.local/bin

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY --chown=bloodchain:bloodchain . .

# Switch to non-root user
USER bloodchain

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

ENTRYPOINT ["gunicorn", "location.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
