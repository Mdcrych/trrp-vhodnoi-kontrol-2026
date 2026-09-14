from pathlib import Path
import csv
import subprocess
import sys
import psycopg
from .config import pg_dsn

CSV_PATH = Path("reports/sales_by_day.csv")
SCRIPT = Path("scripts/render_report.py")

QUERY = """
SELECT s.sold_at, COUNT(*) AS sales_count, SUM(s.quantity) AS items_sold,
       SUM(s.quantity * s.unit_price) AS revenue
FROM sales s
GROUP BY s.sold_at
ORDER BY s.sold_at
"""

def export_report():
    CSV_PATH.parent.mkdir(exist_ok=True)
    with psycopg.connect(pg_dsn()) as conn, conn.cursor() as cur:
        cur.execute(QUERY)
        rows = cur.fetchall()
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Дата", "Количество продаж", "Продано экземпляров", "Выручка, ₽"])
        writer.writerows(rows)
    subprocess.run([sys.executable, str(SCRIPT), str(CSV_PATH), "reports/sales_by_day.xlsx"], check=True)
    return len(rows)
