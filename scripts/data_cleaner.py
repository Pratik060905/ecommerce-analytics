# scripts/data_cleaner.py
import os
import json
import pandas as pd
from config.config import RAW_FOLDER, CLEAN_FOLDER

def clean_json_raw_files():
    os.makedirs(CLEAN_FOLDER, exist_ok=True)
    raw_files = [os.path.join(RAW_FOLDER, f) for f in os.listdir(RAW_FOLDER) if f.endswith(".json")]
    if not raw_files:
        print("[cleaner] No raw JSON files found.")
        return None

    records = []
    for path in raw_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            for it in items:
                # DummyJSON fields: title, price, rating, stock, brand, category, id
                records.append({
                    "product": it.get("title"),
                    "price": float(it.get("price")) if it.get("price") is not None else None,
                    "rating": float(it.get("rating")) if it.get("rating") is not None else None,
                    "website": it.get("brand") or "API",
                    "category": it.get("category"),
                    "stock": int(it.get("stock")) if it.get("stock") is not None else None,
                    "date": pd.Timestamp.now().date()
                })
        except Exception as e:
            print("[cleaner] Error reading", path, e)

    if not records:
        print("[cleaner] No records parsed from raw files.")
        return None

    df = pd.DataFrame(records)

    # Basic cleaning
    df['product'] = df['product'].astype(str).str.strip()
    df = df.dropna(subset=['price'])   # require price
    # Remove duplicates by product+website+date
    if {'product','website','date'}.issubset(df.columns):
        df = df.drop_duplicates(subset=['product','website','date'])

    # Save cleaned CSV
    out_path = os.path.join(CLEAN_FOLDER, "cleaned_combined.csv")
    df.to_csv(out_path, index=False)
    print("[cleaner] Cleaned saved to:", out_path)
    return df
