import os
import sys
import time
from sqlalchemy import create_engine, text


def get_database_url():
    for var in [
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_DB"),
    ]:
        if not var:
            print(f"ERROR: {var} environment variable is not set")
            sys.exit(1)

    db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres-service:5432/postgres"
    return db_url


def wait_for_db(db_url, max_retries=30, retry_interval=2):
    print("Waiting for database to be ready...")

    default_engine = create_engine(
        db_url,
        isolation_level="AUTOCOMMIT",
    )

    with default_engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{os.getenv('POSTGRES_DB')}'")
        )
        exists = result.scalar() is not None

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{os.getenv('POSTGRES_DB')}"'))
            print(f"Database '{os.getenv('POSTGRES_DB')}' created.")
        else:
            print(f"Database '{os.getenv('POSTGRES_DB')}' already exists.")
            
    for attempt in range(max_retries):
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            engine.dispose()
            return True
        except Exception as e:
            print(
                f"Attempt {attempt + 1}/{max_retries}: Database not ready yet... ({e})"
            )
            time.sleep(retry_interval)

    print("ERROR: Database did not become ready in time")
    return False


def main():
    print("=" * 60)
    print("Database Connection Check")
    print("=" * 60)

    db_url = get_database_url()

    if not wait_for_db(db_url):
        sys.exit(1)

    print("=" * 60)
    print("Database is ready for connections!")
    print("=" * 60)


if __name__ == "__main__":
    main()
