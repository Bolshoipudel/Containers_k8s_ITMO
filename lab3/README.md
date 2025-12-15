# Лабораторная №3

## Ход работы

### 1. Установка minikube

- Команда запуска: `minikube start --driver=docker`

![Minikube Start](screenshots/1.%20minikube_start.png)

### 2. Развертывание PostgreSQL

- Созданы манифесты:
  - `pg_secret.yml` - Secret с учетными данными
  - `pg_configmap.yml` - ConfigMap с названием БД
  - `pg_service.yml` - Service типа NodePort
  - `pg_deployment.yml`

![Config View](screenshots/2.%20config_view.png)
![Create Configs](screenshots/3.%20create_configs.png)

### 3. Развертывание Nextcloud

- Созданы манифесты:
  - `nextcloud_configmap.yml` - ConfigMap с переменными окружения
  - `nextcloud.yml` - Secret и Deployment с Liveness/Readiness пробами

![Describe Service](screenshots/4.%20describe_service.png)
![Describe Secret](screenshots/5.%20describe_secret.png)
![Logs](screenshots/6.%20logs.png)

## Ответы на вопросы

### Вопрос 1: Важен ли порядок выполнения манифестов?

Да, важен, т.к. config map'ы (да и секреты) нужно создавать до deployment, так как последний ссылается на config map (и Secret). В данном случае видим:

```yaml
- configMapRef:
    name: postgres-configmap
```

Если сначала не создать ConfigMap, то под просто не запустится. Но service можно при этом создать на любом этапе, т.к. он просто определяет правила маршрутизации к подам по лэйблам. Кубер автоматически подключит service к поднятым подам.

### Вопрос 2: Что произойдет при масштабировании PostgreSQL?

Произойдет следующее: при replicas=0 под с pg удалится, БД будет недоступна, nextcloud потеряет соединение с ней и мы не сможем зайти в nextcloud. Когда отскейлим обратно к 1, создатстся новый под с pg c пустой БД, т.к. мы не используем Persistent Volume, и при пересоздании пода данные удаляются. Nextcloud не будет работать из-за пустой БД и из-за того что был установлен на старую БД. ЧТобы все снова заработало, нужно будет переустановить nextcloud. Ну или даннные восстановить...

![Scale Replicas](screenshots/10.%20scale_replicas.png)

## Скриншоты

Все скриншоты можно найти в директории screenshots
