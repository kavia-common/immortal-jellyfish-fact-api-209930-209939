# syntax=docker/dockerfile:1.6
# Lightweight Python base image suitable for Cloud Run
FROM python:3.12-slim AS base

# Ensure stdout/stderr are unbuffered, set Python path
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

# Set working directory
WORKDIR /app

# System dependencies (if needed in future) and security updates
# Keeping minimal footprint; add build essentials only if required.
RUN apt-get update -y && apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better caching
COPY requirements.txt /app/requirements.txt

# Use pip with no cache for smaller image
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY src /app/src
COPY interfaces /app/interfaces
COPY pyproject.toml /app/pyproject.toml
COPY setup.cfg /app/setup.cfg

# Create a non-root user and group, and own the application directory
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Expose Cloud Run default port
EXPOSE 8080

# Switch to non-root user
USER appuser

# Basic healthcheck hitting the /health endpoint
# Note: Using python -c with urllib to avoid adding curl/wget packages
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python - <<'PY' || exit 1
import sys, urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=2) as r:
        sys.exit(0 if r.status == 200 else 1)
except Exception:
    sys.exit(1)
PY

# Start the ASGI server using uvicorn
# Cloud Run will set PORT env var (defaults to 8080). Bind to 0.0.0.0.
ENV PORT=8080
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT}"]
