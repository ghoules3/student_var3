# Лабораторная работа 2 — Docker / Docker Compose
Бочков Андрей Александрович, БД251‑М  
Вариант 3 (Финансы — Кредитный скоринг)

## Цель
Контейнеризировать аналитическое приложение и оркестрировать сервисы через Docker Compose:
-`db` PostgreSQL для хранения данных
-`loader` init‑контейнер (ETL): загружает CSV в БД и завершает работу
-`analytics_app` JupyterLab для анализа данных из БД

## Архитектура решения
-CSV файл находится на хосте и подключается в `loader` через bind mount read‑only
-Данные PostgreSQL сохраняются в named volume `pg_data`
-Запуск по порядку: `db (healthy)` -> `loader (completed)` -> `analytics_app`

## Требование варианта 3 (Security)
-JupyterLab проброшен только на localhost: `127.0.0.1:8888:8888`
-Доступ в JupyterLab по токену (переменная `JUPYTER_TOKEN` в `.env`)

## Структура проекта
lab_02/
README.md
    project/
    docker-compose.yml
    .env.example
        app/
        Dockerfile
        requirements.txt
        loader.py
        .dockerignore
        data/
        .gitkeep
            notebooks/
            check_db.ipynb
## Датасет
Источник: Kaggle — *Default of Credit Card Clients Dataset*  
https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset

Файл датасета **не коммитится** в репозиторий. Перед запуском положить локально:
- `lab_02/project/data/UCI_Credit_Card.csv`

## Запуск
cd lab_02/project

# создать .env на основе шаблона
cp .env.example .env

# собрать и запустить сервисы
sudo docker compose up -d --build

# проверить статусы
sudo docker compose ps

# посмотреть логи загрузчика
sudo docker compose logs loader

# остановить (тома сохраняются)
sudo docker compose down

# полная очистка (включая volume pg_data)
sudo docker compose down -v

## Проверка результата
# В выводе docker compose ps:
db - healthy
loader - exited(0)
analytics_app - Up

# JupyterLab:
http://127.0.0.1:8888
токен берётся из .env

# Демонстрация чтения из БД:
ноутбук lab_02/project/notebooks/check_db.ipynb
запрос SELECT COUNT(*) возвращает 30000 строк после загрузки датасета

## Скриншоты (docs/lab_02)
-`01_up_build.jpg` - `docker compose up -d --build`  
-`02_ps.jpg` - `docker compose ps --all`  
-`03_loader_logs.jpg` - логи загрузчика  
-`04_ports_localhost.jpg` - порт Jupyter проброшен только на `127.0.0.1`  
-`05_jupyter.jpg` - интерфейс JupyterLab в браузере  
-`06_count_30000.jpg` - запрос `COUNT(*)` в ноутбуке (30000 строк)  
