FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir prometheus-client prometheus-fastapi-instrumentator

USER appuser

COPY main.py .

VOLUME /app/data

EXPOSE 8001:8001

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]