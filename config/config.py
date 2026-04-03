# config/config.py

# SQLite DB path
DB_PATH = "database/ecommerce.db"

# Folders
RAW_FOLDER = "data/raw"
CLEAN_FOLDER = "data/cleaned"

# Keywords (products) to search via API
KEYWORDS = [
    "iphone",
    "samsung",
    "laptop",
    "smartwatch",
    "headphones",
    "oneplus",
    "tablet",
    "camera",
    "printer",
    "monitor",  
    "xiomi",
    "dslr",
    "gaming console",
    "smart speaker",
    "fitness tracker",  
    "drone",
    "external hard drive",  
    "wireless charger",
    "bluetooth speaker"
]


# How many items to keep per keyword (truncate if API returns many)
MAX_ITEMS = 20

# API endpoint (DummyJSON)
PRODUCT_API_SEARCH = "https://dummyjson.com/products/search?q={query}"

# Streamlit cache TTL in seconds
CACHE_TTL = 300


