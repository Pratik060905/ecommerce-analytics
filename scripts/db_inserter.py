# scripts/db_inserter.py
import os
from sqlalchemy import create_engine, text
from config.config import DB_PATH

def ensure_db_and_table():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
    # create table if not exists
    create_stmt = """
    CREATE TABLE IF NOT EXISTS product_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        price REAL,
        rating REAL,
        website TEXT,
        category TEXT,
        stock INTEGER,
        date TEXT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_stmt))
    return engine

def insert_dataframe(df):
    if df is None or df.empty:
        print("[db_inserter] Nothing to insert.")
        return
    engine = ensure_db_and_table()
    # Append rows
    df.to_sql("product_data", con=engine, if_exists="append", index=False)
    print(f"[db_inserter] Inserted {len(df)} rows into DB at {DB_PATH}")
