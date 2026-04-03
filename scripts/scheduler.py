# scripts/scheduler.py
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import schedule
import time
from scripts.etl_pipeline import run_once

def start_scheduler(run_time="09:00"):
    schedule.every().day.at(run_time).do(run_once)
    print(f"[scheduler] Scheduled ETL daily at {run_time}.")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # change time if you want, format "HH:MM" 24-hour
    start_scheduler("09:00")



