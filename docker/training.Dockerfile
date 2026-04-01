FROM fraud-base:1.0.0
WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.training.train"]