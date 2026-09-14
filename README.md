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

## Проверка
Повторный запуск команды `import` безопасен: используются естественные ключи, `ON CONFLICT` и уникальность номера продажи.

Подробности: `docs/SCHEMA.md` и `docs/ALGORITHM.md`.
