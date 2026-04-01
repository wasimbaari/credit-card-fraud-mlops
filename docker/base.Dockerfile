FROM python:3.10-slim

# Security best practice
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (DevSecOps)
RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER appuser