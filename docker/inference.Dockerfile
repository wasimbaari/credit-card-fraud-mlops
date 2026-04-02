FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser
WORKDIR /app

# DO NOT COPY model.joblib here. KServe pulls it from S3.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN chown -R appuser:appuser /app
USER appuser

ENV PYTHONPATH=/app
ENV MODEL_PATH=/mnt/models/model.joblib

EXPOSE 8080

CMD ["uvicorn", "src.inference.predictor:app", "--host", "0.0.0.0", "--port", "8080"]