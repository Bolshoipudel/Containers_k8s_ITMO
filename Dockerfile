FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir prometheus-client prometheus-fastapi-instrumentator

COPY . .

VOLUME /app/data

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD uvicorn shop_api.main:app --host 0.0.0.0 --port 8000