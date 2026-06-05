FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies for web3 and cryptography
RUN apt-get update && apt-get install -y \
    gcc \
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
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r bloodchain && useradd -r -g bloodchain bloodchain

WORKDIR /app

# Copy Python dependencies from builder and fix permissions
COPY --from=builder --chown=bloodchain:bloodchain /opt/venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/app:/opt/venv/lib/python3.11/site-packages \
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

CMD ["python", "app.py"]
