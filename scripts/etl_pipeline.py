# scripts/etl_pipeline.py
# Run this from project root: python scripts/etl_pipeline.py

import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from config.config import KEYWORDS, RAW_FOLDER
from scripts.api_product_fetcher import fetch_product_data
from scripts.data_cleaner import clean_json_raw_files
from scripts.db_inserter import insert_dataframe
from datetime import datetime
import shutil
import time

os.makedirs(RAW_FOLDER, exist_ok=True)

def run_once():
    print("=== ETL START:", datetime.now(), "===")
    # 1) fetch via API for each keyword
    for kw in KEYWORDS:
        print("[ETL] Fetching keyword:", kw)
        try:
            fetch_product_data(kw)
        except Exception as e:
            print("[ETL] Fetch error:", e)
        time.sleep(1)

    # 2) clean JSON -> DataFrame
    df = clean_json_raw_files()
    # 3) insert into DB
    if df is not None and not df.empty:
        insert_dataframe(df)
    else:
        print("[ETL] No cleaned data to insert.")

    # 4) archive raw files (move to raw/archive)
    archive_folder = os.path.join(RAW_FOLDER, "archive")
    os.makedirs(archive_folder, exist_ok=True)
    for f in os.listdir(RAW_FOLDER):
        full = os.path.join(RAW_FOLDER, f)
        if os.path.isfile(full) and not f.startswith("archive"):
            try:
                shutil.move(full, os.path.join(archive_folder, f))
            except Exception as e:
                print("[ETL] Archive move failed for", f, e)

    print("=== ETL END:", datetime.now(), "===\n")

if __name__ == "__main__":
    run_once()
