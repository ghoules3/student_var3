# Лабораторная работа 3 — Kubernetes

Студент: Бочков Андрей Александрович  
Группа: БД251-М  
Вариант: 3 (Финансы — Credit Scoring — Jupyter)

## Цель
Развернуть аналитическое приложение из ЛР2 в Kubernetes с использованием:
- ConfigMap
- Secret
- PersistentVolumeClaim
- Deployment / Service
- Job
- InitContainer
- LivenessProbe / ReadinessProbe

## Состав решения
В папке `k8s/` находятся манифесты:
- `secret.yaml`
- `configmap.yaml`
- `pvc.yaml`
- `db-deployment.yaml`
- `db-service.yaml`
- `app-deployment.yaml`
- `app-service.yaml`
- `loader-job.yaml`

## Что реализовано
- PostgreSQL развернут в Kubernetes
- JupyterLab развернут как приложение
- загрузка CSV выполнена через Job
- конфигурация вынесена в ConfigMap и Secret
- для БД настроен PVC
- для приложения настроены InitContainer, ReadinessProbe и LivenessProbe
- сервис приложения опубликован через NodePort `30007`

## Результат
- JupyterLab доступен через браузер
- данные из CSV загружены в PostgreSQL
- проверка в JupyterLab показывает `COUNT = 30000`
- после удаления pod базы данные сохраняются благодаря PVC

Скриншоты будут добавлены в `docs/lab_03/`.