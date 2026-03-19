# Лабораторная работа 3 Kubernetes  
Бочков Андрей Александрович  
БД251-М  Вариант 3  
  
## Цель работы  
Перенести аналитическое приложение из ЛР2 (Docker Compose) в Kubernetes и развернуть его в локальном кластере Minikube.  
В работе необходимо было:  
-описать Kubernetes-манифесты  
-вынести конфигурацию в `ConfigMap` и `Secret`  
-настроить хранение данных БД через `PersistentVolumeClaim`  
-развернуть PostgreSQL и JupyterLab  
-выполнить загрузку CSV в БД через `Job`  
-настроить `InitContainer`, `ReadinessProbe` и `LivenessProbe`  
-реализовать вариант **NodePort с фиксированным портом `30007`**  
  
## Используемая структура  
В репозитории для ЛР3 используются:  
-`lab_03/README.md` отчет по лабораторной работе 3  
-`lab_03/k8s/` Kubernetes-манифесты  
-`docs/lab_03/` скриншоты выполнения  
-`lab_02/project/app/` Dockerfile и код приложения, переиспользованные из ЛР2  
  
## Архитектура решения  
В Kubernetes развернуты следующие компоненты:  
### 1. База данных  
-**PostgreSQL 16 Alpine**  
-развернута через `Deployment`  
-доступ внутри кластера через `Service` типа `ClusterIP`  
-хранение данных организовано через `PersistentVolumeClaim`  
  
### 2. Аналитическое приложение  
-**JupyterLab**  
-развернуто через `Deployment`  
-опубликовано через `Service` типа `NodePort`  
-фиксированный порт варианта: **30007**  
-доступ к БД выполняется по внутреннему адресу `db-service`  
  
### 3. Загрузка данных  
-реализована через Kubernetes `Job`    
-Job использует CSV-файл `UCI_Credit_Card.csv`  
-после загрузки Job завершается со статусом `Complete`  
  
### 4. Конфигурация  
-несекретные параметры вынесены в `ConfigMap`  
-чувствительные данные вынесены в `Secret`  
  
## Состав Kubernetes-манифестов  
В папке `lab_03/k8s/` созданы следующие файлы:  
-`secret.yaml`  
-`configmap.yaml`  
-`pvc.yaml`  
-`db-deployment.yaml`  
-`db-service.yaml`  
-`app-deployment.yaml`  
-`app-service.yaml`  
-`loader-job.yaml`  
  
## Содержимое манифестов  
### `secret.yaml`  
Содержит чувствительные параметры:  
-`POSTGRES_PASSWORD`  
-`JUPYTER_TOKEN`  
  
### `configmap.yaml`  
Содержит обычные переменные окружения:  
-`POSTGRES_DB`  
-`POSTGRES_USER`  
-`DB_HOST`  
-`DB_PORT`  
-`CSV_PATH`  
-`TABLE_NAME`  
-`CSV_SKIPROWS`  
  
### `pvc.yaml`  
Описывает `PersistentVolumeClaim` для PostgreSQL:  
-`accessMode: ReadWriteOnce`  
-`storage: 1Gi`  
  
### `db-deployment.yaml`  
Разворачивает PostgreSQL и подключает PVC в:  
-`/var/lib/postgresql/data`  
  
### `db-service.yaml`  
Создает сервис базы данных:  
-тип `ClusterIP`  
-порт `5432`  
  
### `app-deployment.yaml`  
Разворачивает JupyterLab и содержит:  
-`initContainer`, ожидающий готовность БД  
-`readinessProbe`  
-`livenessProbe`  
  
### `app-service.yaml`  
Создает сервис приложения:  
-тип `NodePort`  
-порт приложения `8888`  
-фиксированный `nodePort: 30007`  
  
### `loader-job.yaml`  
Описывает однократную загрузку CSV в PostgreSQL через Kubernetes Job.  
  
## Ход выполнения  
### Запуск Minikube  
Кластер был запущен командой:  
```bash  
minikube start --driver=docker  
```  
  
### Сборка образа приложения внутри Minikube  
Для того чтобы Kubernetes мог использовать локальный образ без внешнего registry, была выполнена команда:  
```bash  
eval $(minikube docker-env)  
docker build -t credit-app:latest ./lab_02/project/app  
```
  
### Применение манифестов  
После подготовки кластера были применены манифесты:  
```bash  
kubectl apply -f lab_03/k8s/  
```  
  
### Проверка ресурсов  
Для проверки состояния объектов использовались команды:  
```bash  
kubectl get all  
kubectl get pvc  
kubectl get jobs  
```  
  
### Проверка сервиса приложения  
Для приложения был создан сервис типа NodePort с фиксированным портом:  
```text  
30007  
```  
  
### Проверка загрузки данных  
Job успешно загрузил CSV-файл в PostgreSQL.  
По логам видно:  
- чтение файла UCI_Credit_Card.csv  
- размер DataFrame (30000, 25)  
- загрузку 30000 строк в таблицу credit_default  
  
### Проверка доступа к данным из JupyterLab  
Результат:  
```text  
COUNT = 30000  
```  
  
### Проверка данных  
Для проверки PVC pod базы данных был удален, после чего Kubernetes автоматически создал новый pod.  
Повторная проверка показала, что данные сохранились.  
  
### Реализация требования варианта  
Для варианта 3 требовалось использовать NodePort с фиксированным портом.  
Это требование выполнено в app-service.yaml:  
- тип сервиса: NodePort  
- фиксированный порт: 30007  
  
### Результат  
В результате выполненной работы:  
-PostgreSQL успешно развернут в Kubernetes  
-JupyterLab успешно развернут в Kubernetes  
-данные из CSV загружены в БД через Job  
-конфигурация вынесена в ConfigMap и Secret  
-хранение данных БД обеспечивается через PVC  
-реализованы InitContainer, ReadinessProbe, LivenessProbe  
-приложение доступно через NodePort 30007  
-подтверждено наличие 30000 строк в таблице  
-подтверждена сохранность данных после пересоздания pod базы данных  
  
### Скриншоты  
Скриншоты размещены в папке:  
```text  
docs/lab_03/  
```  
- 01_minikube_start.jpg  
- 02_minikube_status_nodes.jpg  
- 03_kubectl_apply.jpg  
- 04_kubectl_get_all.jpg  
- 05_kubectl_get_pvc.jpg  
- 06_kubectl_get_jobs.jpg  
- 07_loader_logs.jpg  
- 08_app_service_nodeport.jpg  
- 09_jupyter_open.jpg  
- 10_jupyter_count_30000.jpg  
- 11_pod_recreated.jpg  
  
### Вывод  
В лабораторной работе выполнен перенос аналитического приложения из Docker Compose в Kubernetes.  
Реализованы базовые механизмы оркестрации: манифесты, сервисы, Job, PVC, probes, ConfigMap и Secret.  
Приложение работает в кластере Minikube, а данные сохраняются при пересоздании pod базы данных.  
