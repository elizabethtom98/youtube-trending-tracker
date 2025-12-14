# scheduler.py
"""
Simple ETL scheduler script.

Calls the FastAPI batch endpoint /jobs/fetch-multi
to fetch trending videos for multiple regions in one go.

You can run this manually:
    python scheduler.py

Or schedule it with cron (see README / instructions).
"""

import os
import sys
import datetime as dt
import requests

# Base URL of your FastAPI app
API_BASE = os.getenv("YT_API_BASE", "http://127.0.0.1:8000")

# Default regions (must match your FastAPI DEFAULT_REGIONS if you like)
DEFAULT_REGIONS = os.getenv("YT_REGIONS", "AU,IN,US,CA,GB").split(",")

def run_batch_job():
    print(f"[{dt.datetime.utcnow().isoformat()}] Starting batch ETL job...")

    # Build query params: regions=AU&regions=IN&...&max_results=50
    params = [("regions", r.strip()) for r in DEFAULT_REGIONS if r.strip()]
    params.append(("max_results", "50"))

    url = f"{API_BASE}/jobs/fetch-multi"
    try:
        resp = requests.post(url, params=params, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to call {url}: {e}", file=sys.stderr)
        return

    data = resp.json()
    print(f"[INFO] Batch job response: {data}")

    # Optional: nice summary print
    jobs = data.get("jobs", [])
    for job in jobs:
        region = job.get("region")
        fetched = job.get("fetched")
        upserted = job.get("upserted")
        captured = job.get("capturedAt")
        print(f"  - {region}: fetched={fetched}, upserted={upserted}, capturedAt={captured}")

    print(f"[{dt.datetime.utcnow().isoformat()}] Batch ETL job complete.")


if __name__ == "__main__":
    run_batch_job()
