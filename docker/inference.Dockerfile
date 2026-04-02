FROM python:3.10-slim

# ---- Minimal packages ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Create non-root user ----
RUN useradd -m -u 10001 appuser

# ---- Set working directory ----
WORKDIR /app

# ---- Copy requirements first (better caching) ----
COPY requirements.txt .

# ---- Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application code ----
COPY src/ ./src/

# ---- 🔥 COPY MODEL (CRITICAL FIX) ----
COPY model.joblib /app/model.joblib

# ---- Set permissions ----
RUN chown -R appuser:appuser /app

# ---- Switch to non-root user ----
USER appuser

# ---- Environment ----
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/model.joblib   # ✅ FIXED

# ---- Expose port ----
EXPOSE 8080

# ---- Run server ----
CMD ["uvicorn", "src.inference.predictor:app", "--host", "0.0.0.0", "--port", "8080"]