# -----------------------------
# Base Image (official, stable)
# -----------------------------
FROM python:3.10-slim

# -----------------------------
# Security (non-root user)
# -----------------------------
RUN useradd -m appuser

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# System deps (needed for ML libs)
# -----------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy project
# -----------------------------
COPY . .

# -----------------------------
# Environment
# -----------------------------
ENV PYTHONPATH=/app

# -----------------------------
# Switch to non-root
# -----------------------------
USER appuser

# -----------------------------
# Run training
# -----------------------------
CMD ["python", "-m", "src.training.train"]