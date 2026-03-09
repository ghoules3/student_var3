#!/usr/bin/env python3
import os
import sys
import time

import pandas as pd
from sqlalchemy import create_engine, text


def wait_for_db(db_url: str, max_retries: int = 30, delay: int = 2) -> None:
    print("[loader] Waiting for PostgreSQL...")
    for attempt in range(1, max_retries + 1):
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            print(f"[loader] DB is available (attempt {attempt})")
            return
        except Exception as e:
            print(f"[loader] DB not ready (attempt {attempt}/{max_retries}): {e}")
            time.sleep(delay)
    print("[loader] DB is not available. Exiting.")
    sys.exit(1)


def main() -> None:
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "creditdb")
    db_user = os.getenv("POSTGRES_USER", "credit_user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "credit_pass")

    csv_path = os.getenv("CSV_PATH", "/data/UCI_Credit_Card.csv")
    table_name = os.getenv("TABLE_NAME", "credit_default")
    skiprows = int(os.getenv("CSV_SKIPROWS", "0"))

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    wait_for_db(db_url)

    engine = create_engine(db_url)

    with engine.connect() as conn:
        try:
            cnt = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}";')).scalar()
            if cnt and int(cnt) > 0:
                print(f"[loader] Table '{table_name}' already has {cnt} rows. Skipping load.")
                return
        except Exception:
            pass

    print(f"[loader] Reading CSV: {csv_path} (skiprows={skiprows})")
    df = pd.read_csv(csv_path, skiprows=skiprows) if skiprows > 0 else pd.read_csv(csv_path)

    df.columns = [c.strip().replace(".", "_").replace(" ", "_") for c in df.columns]

    print(f"[loader] DataFrame shape: {df.shape}")
    print(f"[loader] Loading into table '{table_name}' (append)...")

    df.to_sql(table_name, engine, if_exists="append", index=False)

    with engine.connect() as conn:
        cnt = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}";')).scalar()
    print(f"[loader] Loaded rows into '{table_name}': {cnt}")
    print("[loader] Done.")


if __name__ == "__main__":
    main()