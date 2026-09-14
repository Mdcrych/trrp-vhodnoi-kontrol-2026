import argparse
import subprocess
from pathlib import Path
from .create_source_db import create_source_db
from .importer import import_data
from .exporter import export_report
from .config import pg_dsn

def init_schema():
    schema = Path("sql/001_schema.sql")
    subprocess.run(["psql", pg_dsn(), "-f", str(schema)], check=True)

def main():
    parser = argparse.ArgumentParser(description="Импорт SQLite → PostgreSQL → XLSX")
    parser.add_argument("command", choices=["create-source", "init-schema", "import", "export"])
    args = parser.parse_args()
    if args.command == "create-source":
        print(f"Создана SQLite БД: {create_source_db()}")
    elif args.command == "init-schema":
        init_schema(); print("Схема PostgreSQL создана")
    elif args.command == "import":
        print(f"Импортировано строк: {import_data()}")
    else:
        print(f"Экспортировано строк отчёта: {export_report()}")

if __name__ == "__main__":
    main()
