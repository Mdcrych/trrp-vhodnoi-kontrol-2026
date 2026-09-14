from pathlib import Path
import csv
import sqlite3
import subprocess
import sys

import psycopg

from .config import pg_dsn
from .importer import SOURCE

REPORTS = Path("reports")
RENDER_SCRIPT = Path("scripts/render_report.py")


def write_csv(path: Path, headers, rows):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def render_xlsx(csv_path: Path, xlsx_path: Path, sheet_name: str, title: str):
    subprocess.run(
        [sys.executable, str(RENDER_SCRIPT), str(csv_path), str(xlsx_path), sheet_name, title],
        check=True,
    )


def export_source_files():
    if not SOURCE.exists():
        raise FileNotFoundError("Нет SQLite-файла. Выполните create-source.")

    with sqlite3.connect(SOURCE) as conn:
        cursor = conn.execute("SELECT * FROM sales_flat ORDER BY sale_number")
        headers = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

    csv_path = REPORTS / "01_source_denormalized.csv"
    xlsx_path = REPORTS / "01_source_denormalized.xlsx"

    write_csv(csv_path, headers, rows)
    render_xlsx(
        csv_path,
        xlsx_path,
        "Исходные данные",
        "Шаг 1. Ненормализованные данные SQLite",
    )
    return len(rows), csv_path, xlsx_path


NORMALIZED_QUERY = """
SELECT
    s.sale_number AS "Номер продажи",
    s.sold_at AS "Дата продажи",
    c.full_name AS "Покупатель",
    c.phone AS "Телефон",
    e.full_name AS "Сотрудник",
    b.isbn AS "ISBN",
    b.title AS "Книга",
    g.name AS "Жанр",
    STRING_AGG(a.full_name, ', ' ORDER BY a.full_name) AS "Авторы",
    s.quantity AS "Количество",
    s.unit_price AS "Цена, ₽",
    s.quantity * s.unit_price AS "Сумма, ₽"
FROM sales s
JOIN customers c ON c.customer_id = s.customer_id
JOIN employees e ON e.employee_id = s.employee_id
JOIN books b ON b.book_id = s.book_id
JOIN genres g ON g.genre_id = b.genre_id
JOIN book_authors ba ON ba.book_id = b.book_id
JOIN authors a ON a.author_id = ba.author_id
GROUP BY s.sale_id, c.customer_id, e.employee_id, b.book_id, g.genre_id
ORDER BY s.sale_number
"""


def export_normalized_files():
    with psycopg.connect(pg_dsn()) as conn, conn.cursor() as cur:
        cur.execute(NORMALIZED_QUERY)
        headers = [column.name for column in cur.description]
        rows = cur.fetchall()

    csv_path = REPORTS / "02_normalized_data.csv"
    xlsx_path = REPORTS / "02_normalized_data.xlsx"

    write_csv(csv_path, headers, rows)
    render_xlsx(
        csv_path,
        xlsx_path,
        "Нормализованные данные",
        "Шаг 2. Данные после нормализации PostgreSQL",
    )
    return len(rows), csv_path, xlsx_path


REPORT_QUERY = """
SELECT
    s.sold_at,
    COUNT(*) AS sales_count,
    SUM(s.quantity) AS items_sold,
    SUM(s.quantity * s.unit_price) AS revenue
FROM sales s
GROUP BY s.sold_at
ORDER BY s.sold_at
"""


def export_report():
    with psycopg.connect(pg_dsn()) as conn, conn.cursor() as cur:
        cur.execute(REPORT_QUERY)
        rows = cur.fetchall()

    headers = [
        "Дата",
        "Количество продаж",
        "Продано экземпляров",
        "Выручка, ₽",
    ]

    csv_path = REPORTS / "03_sales_by_day.csv"
    xlsx_path = REPORTS / "03_sales_by_day.xlsx"

    write_csv(csv_path, headers, rows)
    render_xlsx(
        csv_path,
        xlsx_path,
        "Продажи по дням",
        "Шаг 3. Отчёт: продажи по дням",
    )
    return len(rows), csv_path, xlsx_path
