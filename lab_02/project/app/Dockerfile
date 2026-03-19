# ============================================================
# Вариант 3 / Credit scoring / Jupyter
# ============================================================

# 1. Конкретная версия slim-образа (не latest)
FROM python:3.10-slim

# 2. Метаданные
LABEL maintainer="student" \
      description="Credit scoring: ETL loader + JupyterLab analytics app"

# 3. Установка системных зависимостей + очистка кэша в одном слое
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 4. Создание непривилегированного пользователя (UID 1000)
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 -m appuser

# 5. Рабочая директория
WORKDIR /app

# 6. Копирование и установка зависимостей до кода (кэш слоёв)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. Копирование кода приложения
COPY loader.py ./

# 8. Создать writable каталог для Jupyter
RUN mkdir -p /home/appuser/work && chown -R appuser:appuser /home/appuser

# 9. Переключение на непривилегированного пользователя
USER appuser

# 10. Рабочая директория для Jupyter
WORKDIR /home/appuser/work

# 11. Порт JupyterLab
EXPOSE 8888

# 12. Точка входа по умолчанию — JupyterLab
CMD ["bash", "-lc", "jupyter lab --ServerApp.root_dir=/home/appuser/work --ServerApp.token=${JUPYTER_TOKEN} --ServerApp.password='' --ip=0.0.0.0 --port=8888 --no-browser"]