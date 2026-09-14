CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS authors (
    author_id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS books (
    book_id BIGSERIAL PRIMARY KEY,
    isbn TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    genre_id BIGINT NOT NULL REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id BIGINT NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES authors(author_id) ON DELETE RESTRICT,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id BIGSERIAL PRIMARY KEY,
    sale_number TEXT NOT NULL UNIQUE,
    sold_at DATE NOT NULL,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    employee_id BIGINT NOT NULL REFERENCES employees(employee_id),
    book_id BIGINT NOT NULL REFERENCES books(book_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0)
);

CREATE INDEX IF NOT EXISTS idx_sales_sold_at ON sales(sold_at);
