# Лабораторная №4

## 1. Запуск

- Рекомендуется использовать скрипт [`run.sh`](./run.sh).
- Для ручного запуска необходимо выполнить следующие команды:

  ```bash

  minikube start --driver=docker
  eval $(minikube docker-env)

  docker build -t shop-db-init:latest init/
  docker build -t shop-api:latest shop_api/

  cd manifests/

  kubectl apply -f pg_configmap.yml
  kubectl apply -f shop_configmap.yml
  kubectl apply -f pg_secret.yml
  kubectl apply -f shop_secret.yml

  kubectl apply -f pg_deployment.yml
  kubectl apply -f pg_service.yml

  kubectl apply -f shop_deployment.yml
  kubectl apply -f shop_service.yml

  kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

  kubectl get deployment shop
  kubectl get pods -l app=shop

  kubectl get pods
  kubectl get services

  minikube service shop-service --url
  ```

## 2. Манифесты для развертывания PostgreSQL

- `pg_secret.yml` - Secret с учетными данными
- `pg_configmap.yml` - ConfigMap с названием БД
- `pg_service.yml` - Service типа NodePort
- `pg_deployment.yml`

## 3. Манифесты для развертывания API

- `shop_secret.yml` - Secret с учетными данными
- `shop_configmap.yml` - ConfigMap с используемой БД и портом
- `shop_service.yml` - Service типа NodePort
- `shop_deployment.yml`

## Скриншоты

Все скриншоты успешного развертывания можно найти в директории [`screenshots`](./screenshots/).
