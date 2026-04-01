FROM fraud-base:latest

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.training.train"]