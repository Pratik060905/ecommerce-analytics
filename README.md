# Automated E-Commerce Price Intelligence Dashboard

## Overview
Automated pipeline to collect product prices from multiple e-commerce sites (Amazon, Flipkart), clean and store them in SQLite, and visualize via Streamlit.

## Run locally
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python scripts/etl_pipeline.py   # run once
5. streamlit run dashboard/dashboard_app.py

## Automate
- Use python scripts/scheduler.py (runs while machine is on) or crontab to run scripts/etl_pipeline.py daily.

## Notes
- Respect sites' terms and rate limits.
- Use FakeStoreAPI fallback if scraping fails.
 
