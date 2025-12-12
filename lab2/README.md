**Лабораторная работа №2**

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