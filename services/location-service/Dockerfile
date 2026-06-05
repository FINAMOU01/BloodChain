FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir --default-timeout=300 --retries=5 -r requirements.txt

# ── Runtime stage ──
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    libpq5 \
    libgdal36 \
    libproj25 \
    binutils \
    && ln -s /usr/lib/x86_64-linux-gnu/libgdal.so.36 /usr/lib/x86_64-linux-gnu/libgdal.so \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with a real home directory
RUN groupadd -r bloodchain && useradd -r -g bloodchain -m -d /home/bloodchain bloodchain

WORKDIR /app

# Copy Python dependencies into bloodchain's home instead of root's
COPY --from=builder --chown=bloodchain:bloodchain /root/.local /home/bloodchain/.local

ENV PATH=/home/bloodchain/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --chown=bloodchain:bloodchain . .

USER bloodchain

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]