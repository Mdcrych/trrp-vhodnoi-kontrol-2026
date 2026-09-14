# Входной контроль — импорт и экспорт данных

Проект реализует требования входного контроля: импорт строк из ненормализованной SQLite БД в нормализованную PostgreSQL БД и экспорт отчёта в XLSX.

## Предметная область
Книжный магазин. Ненормализованная таблица `sales_flat` хранит продажу, покупателя, книгу, автора, жанр, сотрудника и количество в одной строке. PostgreSQL хранит сущности раздельно.

## Структура
- `sql/001_schema.sql` — скрипт создания 7 таблиц PostgreSQL.
- `src/create_source_db.py` — формирование SQLite с демонстрационными строками.
- `src/importer.py` — импорт без преобразования бизнес-значений.
- `src/exporter.py` — подготовка CSV и запуск отдельного приложения.
- `scripts/render_report.py` — создаёт и форматирует XLSX.

## Быстрый запуск
```bash
cp .env.example .env
docker compose up -d db
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main create-source
python -m src.main init-schema
python -m src.main import
python -m src.main export
```

Итоговый файл: `reports/sales_by_day.xlsx`.

## Контейнерный запуск
```bash
docker compose run --rm app create-source
docker compose run --rm app init-schema
docker compose run --rm app import
docker compose run --rm app export
```

## Наглядный запуск

Одна команда последовательно:

1. Генерирует SQLite-файл с ненормализованной таблицей.
2. Выгружает исходные данные в CSV и XLSX.
3. Создаёт нормализованную схему PostgreSQL.
4. Импортирует данные в таблицы PostgreSQL.
5. Выгружает нормализованную витрину в CSV и XLSX.
6. Формирует итоговый отчёт по продажам в CSV и XLSX.

```bash
cd ~/trrp-vhodnoi-kontrol-2026

git pull origin main

source .venv/bin/activate

set -a
source .env
set +a

docker compose up -d db

python -m src.main demo

ls -lh reports/
```

После запуска открой файлы:

```bash
xdg-open reports/01_source_denormalized.xlsx
xdg-open reports/02_normalized_data.xlsx
xdg-open reports/03_sales_by_day.xlsx
```

## Проверка
Повторный запуск команды `import` безопасен: используются естественные ключи, `ON CONFLICT` и уникальность номера продажи.

Подробности: `docs/SCHEMA.md` и `docs/ALGORITHM.md`.
