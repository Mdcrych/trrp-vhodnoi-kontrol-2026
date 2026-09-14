from pathlib import Path
import sqlite3
import psycopg
from .config import pg_dsn

SOURCE = Path("data/source_bookstore.db")

def rows_from_source():
    if not SOURCE.exists():
        raise FileNotFoundError("Нет SQLite-файла. Выполните create-source.")
    with sqlite3.connect(SOURCE) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM sales_flat ORDER BY sale_number").fetchall()

def value_id(cur, table, column, value):
    cur.execute(f"INSERT INTO {table} ({column}) VALUES (%s) ON CONFLICT ({column}) DO UPDATE SET {column} = EXCLUDED.{column} RETURNING {table[:-1]}_id", (value,))
    return cur.fetchone()[0]

def import_data():
    rows = rows_from_source()
    with psycopg.connect(pg_dsn()) as conn:
        with conn.cursor() as cur:
            for row in rows:
                customer_id = value_id(cur, "customers", "full_name", row["customer_name"])
                cur.execute("UPDATE customers SET phone=%s WHERE customer_id=%s AND phone=%s", (row["customer_phone"], customer_id, row["customer_phone"]))
                employee_id = value_id(cur, "employees", "full_name", row["employee_name"])
                genre_id = value_id(cur, "genres", "name", row["genre_name"])
                author_id = value_id(cur, "authors", "full_name", row["author_name"])
                cur.execute("""INSERT INTO books (isbn, title, genre_id) VALUES (%s, %s, %s)
                    ON CONFLICT (isbn) DO UPDATE SET title=EXCLUDED.title, genre_id=EXCLUDED.genre_id
                    RETURNING book_id""", (row["isbn"], row["book_title"], genre_id))
                book_id = cur.fetchone()[0]
                cur.execute("INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (book_id, author_id))
                cur.execute("""INSERT INTO sales (sale_number, sold_at, customer_id, employee_id, book_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (sale_number) DO NOTHING""",
                    (row["sale_number"], row["sold_at"], customer_id, employee_id, book_id, row["quantity"], row["unit_price"]))
    return len(rows)
