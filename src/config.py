import os


def pg_dsn() -> str:
    keys = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
    values = {key: os.getenv(key) for key in keys}
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise RuntimeError(f"Не заданы переменные окружения: {', '.join(missing)}")
    return " ".join(f"{key[2:].lower()}={value}" for key, value in values.items())
