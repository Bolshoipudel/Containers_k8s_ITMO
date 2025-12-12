FROM python:3.12-slim

WORKDIR /init

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" inituser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER inituser

COPY init_db.py .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "init_db.py"]
