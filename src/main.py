import argparse
import subprocess
from pathlib import Path

from .config import pg_dsn
from .create_source_db import create_source_db
from .exporter import (
    export_best_employee,
    export_largest_sale_by_day,
    export_normalized_files,
    export_normalized_structure,
    export_report,
    export_source_files,
)
from .importer import import_data


def init_schema():
    """Применяет SQL-скрипт создания таблиц PostgreSQL."""
    schema = Path("sql/001_schema.sql")

    subprocess.run(
        [
            "psql",
            pg_dsn(),
            "-f",
            str(schema),
        ],
        check=True,
    )


def print_files(label, result):
    """Красиво выводит в терминал список созданных файлов."""
    count, csv_path, xlsx_path = result

    print(f"{label}: {count} строк")
    print(f"  CSV:  {csv_path}")
    print(f"  XLSX: {xlsx_path}")


def demo():
    """
    Запускает весь сценарий для демонстрации преподавателю.

    Порядок:
    1. Создание SQLite-источника.
    2. Экспорт ненормализованных данных.
    3. Создание PostgreSQL-схемы.
    4. Импорт и нормализация.
    5. Экспорт витрины и структуры PostgreSQL.
    6. Создание аналитических отчётов.
    """
    print("=== Шаг 1. Ненормализованный источник SQLite ===")

    print(f"SQLite БД: {create_source_db()}")

    print_files(
        "Исходные данные выгружены",
        export_source_files(),
    )

    print()
    print("=== Шаг 2. Нормализация в PostgreSQL ===")

    init_schema()

    print(
        f"Импортировано строк из SQLite: "
        f"{import_data()}"
    )

    print_files(
        "Витрина нормализованных данных выгружена",
        export_normalized_files(),
    )

    sheet_count, structure_path = export_normalized_structure()

    print(
        f"Структура нормализованной БД: "
        f"{sheet_count} листов"
    )

    print(f"  XLSX: {structure_path}")

    print()
    print("=== Шаг 3. Аналитические отчёты ===")

    print_files(
        "Отчёт по продажам за дни",
        export_report(),
    )

    print_files(
        "Самый эффективный сотрудник",
        export_best_employee(),
    )

    print_files(
        "Самая большая продажа каждого дня",
        export_largest_sale_by_day(),
    )

    print()
    print("Готово. Все результаты находятся в каталоге reports/.")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Демонстрация: SQLite → PostgreSQL → "
            "наглядные CSV/XLSX-отчёты"
        )
    )

    parser.add_argument(
        "command",
        choices=[
            "create-source",
            "export-source",
            "init-schema",
            "import",
            "export-normalized",
            "export-structure",
            "export",
            "export-analytics",
            "demo",
        ],
    )

    args = parser.parse_args()

    if args.command == "create-source":
        print(f"Создана SQLite БД: {create_source_db()}")

    elif args.command == "export-source":
        print_files(
            "Исходные данные выгружены",
            export_source_files(),
        )

    elif args.command == "init-schema":
        init_schema()
        print("Схема PostgreSQL создана")

    elif args.command == "import":
        print(f"Импортировано строк: {import_data()}")

    elif args.command == "export-normalized":
        print_files(
            "Витрина нормализованных данных выгружена",
            export_normalized_files(),
        )

    elif args.command == "export-structure":
        sheet_count, path = export_normalized_structure()

        print(
            f"Структура нормализованной БД: "
            f"{sheet_count} листов"
        )

        print(f"XLSX: {path}")

    elif args.command == "export":
        print_files(
            "Отчёт по продажам за дни",
            export_report(),
        )

    elif args.command == "export-analytics":
        print_files(
            "Самый эффективный сотрудник",
            export_best_employee(),
        )

        print_files(
            "Самая большая продажа каждого дня",
            export_largest_sale_by_day(),
        )

    else:
        demo()


if __name__ == "__main__":
    main()
