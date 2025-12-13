# Лабораторная работа №2

## Описание работы

Трёхсервисная архитектура магазина:

1. **postgres** - PostgreSQL 15, persistent хранилище с healthcheck
2. **db-init** - one-shot контейнер для инициализации БД (запускается после postgres, завершается после выполнения)
3. **shop-api** - FastAPI приложение на порту 8001, стартует после успешной инициализации БД

**Зависимости:** db-init → postgres (healthy) → shop-api → оба предыдущих

**Volumes:**

- `postgres-data` - БД
- `shop-data` - данные приложения

**Network:** единая bridge-сеть `shop-network`

Все переменные окружения берутся из `.env` файла.

## Ответы на вопросы

### Можно ли ограничивать ресурсы (например, память или CPU) для сервисов в docker-compose.yml? Если нет, то почему если да, то как?

Да, ограничиnm CPU и память на уровне контейнера, возможно

```yaml
version: "3"

services:
  something:
    image: something
    deploy:
      replicas: 3 # Встроенная балансировка
      resources:
        limits:
          cpus: "1.0" # Лимит CPU
          memory: 512M # Лимит по памяти
        reservations:
          cpus: "0.25"
          memory: 128M
```

Однако стоит упомянуть, что спецификация :deploy предназначена для режима swarm. И при запуске `docker compose up something`

Если же нужно ограничить в обычном `docker compose`, можно использовать (что в свою очередь, кажется уже устарело, исходя из различных источников)

```yaml
services:
  something:
    image: something
    mem_limit: 512m
    mem_reservation: 128m
    cpus: 1.0
```

### Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные?

- Запустить сервис вместе с его зависемостиями (depends on):

    ```bash
    docker compose up single_server
    ```

- Также можно запустить несколько сервисов

    ```bash
    docker compose up first_server second_server ...
    ```

- Запустить сервис без зависемостей:

    ```bash
    docker compose up --no-deps single_server
    ```
