import os


def pg_dsn() -> str:
    mapping = {
        "PGHOST": "host",
        "PGPORT": "port",
        "PGDATABASE": "dbname",
        "PGUSER": "user",
        "PGPASSWORD": "password",
    }
    values = {env_name: os.getenv(env_name) for env_name in mapping}
    missing = [env_name for env_name, value in values.items() if not value]
    if missing:
        raise RuntimeError(f"Не заданы переменные окружения: {', '.join(missing)}")
    return " ".join(f"{mapping[env_name]}={value}" for env_name, value in values.items())
