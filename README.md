# DevOps — ЛР 1 (Вариант 3)

Студент: Бочков Андрей Александрович, БД251-м

Цель: отработать Git-процессы (ветки, merge-конфликт, stash, PR) и подготовить requirements.txt под ML-стек (финансы/скоринг).  
Данные: датасет Kaggle "Default of Credit Card Clients" (в data/, в Git не коммитится).

Структура:
- data/ — данные (raw/processed), в Git игнорируется
- src/ — исходный код (скрипты)
- notebooks/ — ноутбуки (опционально)
- docs/ — скриншоты/отчёт

Ветки:
- main
- dev
- feature/data-loader - правки src/loader.py, спровоцирован конфликт при merge в dev
- feature/requirements - подготовка requirements.txt и демонстрация git stash

Pull request: dev → main (https://github.com/ghoules3/student_var3/pull/1)

ML‑стек: numpy, pandas, scikit-learn, matplotlib, seaborn, pyarrow, requests, xgboost

Скриншоты смотреть в папке docs/
