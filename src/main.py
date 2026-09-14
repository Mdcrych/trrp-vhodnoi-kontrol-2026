import argparse
import subprocess
from pathlib import Path

from .config import pg_dsn
from .create_source_db import create_source_db
from .exporter import (
    export_normalized_files,
    export_report,
    export_source_files,
)
from .importer import import_data


def init_schema():
    schema = Path("sql/001_schema.sql")
    subprocess.run(["psql", pg_dsn(), "-f", str(schema)], check=True)


def print_files(label, result):
    count, csv_path, xlsx_path = result
    print(f"{label}: {count} строк")
    print(f"  CSV:  {csv_path}")
    print(f"  XLSX: {xlsx_path}")


def demo():
    print("=== Шаг 1. Генерация ненормализованной SQLite БД ===")
    print(f"SQLite БД: {create_source_db()}")
    print_files("Исходные данные выгружены", export_source_files())

    print("=== Шаг 2. Создание нормализованной PostgreSQL схемы ===")
    init_schema()
    print(f"Импортировано строк из SQLite: {import_data()}")
    print_files(
        "Нормализованные данные выгружены",
        export_normalized_files(),
    )

    print("=== Шаг 3. Формирование итогового отчёта ===")
    print_files("Отчёт выгружен", export_report())

    print("Готово. Откройте каталог reports/.")


def main():
    parser = argparse.ArgumentParser(
        description="Демонстрация: SQLite → PostgreSQL → CSV/XLSX"
    )
    parser.add_argument(
        "command",
        choices=[
            "create-source",
            "export-source",
            "init-schema",
            "import",
            "export-normalized",
            "export",
            "demo",
        ],
    )
    args = parser.parse_args()

    if args.command == "create-source":
        print(f"Создана SQLite БД: {create_source_db()}")

    elif args.command == "export-source":
        print_files("Исходные данные выгружены", export_source_files())

    elif args.command == "init-schema":
        init_schema()
        print("Схема PostgreSQL создана")

    elif args.command == "import":
        print(f"Импортировано строк: {import_data()}")

    elif args.command == "export-normalized":
        print_files(
            "Нормализованные данные выгружены",
            export_normalized_files(),
        )

    elif args.command == "export":
        print_files("Отчёт выгружен", export_report())

    else:
        demo()


if __name__ == "__main__":
    main()
