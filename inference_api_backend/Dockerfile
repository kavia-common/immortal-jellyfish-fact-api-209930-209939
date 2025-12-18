# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source
COPY src /app/src
COPY interfaces /app/interfaces

# Set ownership
RUN chown -R app:app /app
USER app

EXPOSE 3001

# Run uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "3001"]
