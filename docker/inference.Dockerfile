# Use a slim, versioned base image for security and speed
FROM python:3.10-slim

# ---- 1. System Dependencies ----
# Install only what's necessary to build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- 2. Security: Non-Root User ----
# Run as non-root to prevent container breakout exploits
RUN useradd -m -u 10001 appuser

# ---- 3. Environment & Workspace ----
WORKDIR /app
ENV PYTHONPATH=/app
# KServe standard mount point for S3 models
ENV MODEL_PATH=/mnt/models/model.joblib 

# ---- 4. Dependency Management ----
# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- 5. Application Code ----
# Copy only the serving logic, NOT the model weights
COPY src/ ./src/

# ---- 6. Permissions ----
RUN chown -R appuser:appuser /app
USER appuser

# ---- 7. Execution ----
EXPOSE 8080

# Use Uvicorn to serve the FastAPI/Flask app
CMD ["uvicorn", "src.inference.predictor:app", "--host", "0.0.0.0", "--port", "8080"]