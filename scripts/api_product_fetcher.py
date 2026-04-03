# scripts/api_product_fetcher.py
import requests
import json
import os
from datetime import datetime
from config.config import RAW_FOLDER, PRODUCT_API_SEARCH, MAX_ITEMS

def fetch_product_data(keyword):
    os.makedirs(RAW_FOLDER, exist_ok=True)
    q = keyword.replace(' ', '+')
    url = PRODUCT_API_SEARCH.format(query=q)
    print(f"[API] Fetching: {url}")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"[API] Non-200 status for {keyword}: {r.status_code}")
            return None
        data = r.json()
        products = data.get("products", [])
        if not products:
            print(f"[API] No products returned for {keyword}")
            return None

        # trim to MAX_ITEMS
        products = products[:MAX_ITEMS]

        filename = f"{RAW_FOLDER}/{keyword.replace(' ','_')}_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"[API] Saved raw JSON: {filename}")
        return filename
    except Exception as e:
        print("[API] Exception while fetching:", e)
        return None
