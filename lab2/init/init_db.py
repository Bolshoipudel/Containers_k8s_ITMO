
import os
import sys
import time
from sqlalchemy import create_engine, text


def get_database_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable is not set")
        sys.exit(1)
    return db_url


def wait_for_db(db_url, max_retries=30, retry_interval=2):
    print("Waiting for database to be ready...")

    sync_url = db_url.replace("postgresql://", "postgresql+psycopg2://")

    for attempt in range(max_retries):
        try:
            engine = create_engine(sync_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            engine.dispose()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet... ({e})")
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
