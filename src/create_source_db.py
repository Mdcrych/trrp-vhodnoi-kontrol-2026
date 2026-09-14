from pathlib import Path
import sqlite3

SOURCE = Path("data/source_bookstore.db")

ROWS = [
    ("S-1001", "2026-09-01", "Иван Петров", "+79990000001", "Анна Орлова", "978-5-00001-001-1", "Путь DevOps", "Технологии", "Сергей Иванов", 1, 1490.00),
    ("S-1002", "2026-09-01", "Мария Соколова", "+79990000002", "Анна Орлова", "978-5-00001-002-8", "Python для автоматизации", "Технологии", "Сергей Иванов", 2, 1290.00),
    ("S-1003", "2026-09-02", "Иван Петров", "+79990000001", "Дмитрий Волков", "978-5-00001-003-5", "Космическая станция", "Фантастика", "Елена Смирнова", 1, 990.00),
    ("S-1004", "2026-09-02", "Ольга Миронова", "+79990000003", "Дмитрий Волков", "978-5-00001-001-1", "Путь DevOps", "Технологии", "Сергей Иванов", 1, 1490.00)
]


def create_source_db() -> Path:
    SOURCE.parent.mkdir(exist_ok=True)
    with sqlite3.connect(SOURCE) as conn:
        conn.execute("DROP TABLE IF EXISTS sales_flat")
        conn.execute("""
            CREATE TABLE sales_flat (
                sale_number TEXT PRIMARY KEY, sold_at TEXT NOT NULL, customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL, employee_name TEXT NOT NULL, isbn TEXT NOT NULL,
                book_title TEXT NOT NULL, genre_name TEXT NOT NULL, author_name TEXT NOT NULL,
                quantity INTEGER NOT NULL, unit_price REAL NOT NULL
            )
        """)
        conn.executemany("INSERT INTO sales_flat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ROWS)
    return SOURCE
