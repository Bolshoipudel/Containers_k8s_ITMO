echo "Запуск развертывания API для магазина в Kubernetes."

minikube start
eval $(minikube docker-env)

echo ""
echo "Собираем необходимые Docker images."

docker build -t shop-db-init:latest init/
docker build -t shop-api:latest shop_api/

echo ""
echo "Переходим к инициализации манифестов."

cd manifests/

echo "Создание ConfigMaps и Secrets."

kubectl apply -f pg_configmap.yml
kubectl apply -f shop_configmap.yml
kubectl apply -f pg_secret.yml
kubectl apply -f shop_secret.yml

echo "Развертывание Postgres и API магазина"

kubectl apply -f pg_deployment.yml
kubectl apply -f pg_service.yml

kubectl apply -f shop_deployment.yml
kubectl apply -f shop_service.yml

echo "Ожидание готовности PostgreSQL для начала работы."

kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

echo "Проверка запуска pod'ов."

kubectl get deployment shop
kubectl get pods -l app=shop

kubectl get pods
kubectl get services

echo ""
echo "Сервис развернут и доступен по адресу: "

minikube service shop-service --url