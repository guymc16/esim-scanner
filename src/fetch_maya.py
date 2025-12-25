import requests
from requests.auth import HTTPBasicAuth
import json
import os
import time
import argparse
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FEED_FILE = DATA_DIR / "maya_feed.json"

API_KEY = "YUq15J3kizpf"
API_SECRET = "bgiSXZ1qoh9JOzj8N28sB0u1IeaNb3dQGMn6cfYrgLDyr5vLMAzdJVDxFkOtmv3i"
URL = "https://api.maya.net/partners/v1/products"

def fetch_maya_plans(force=False):
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Check Cache
    if not force and FEED_FILE.exists():
        mtime = FEED_FILE.stat().st_mtime
        age_hours = (time.time() - mtime) / 3600
        if age_hours < 24:
            print(f"[CACHE] Maya feed is fresh ({age_hours:.1f} hours old). Loading from disk.")
            with open(FEED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"[CACHE] Maya feed is stale ({age_hours:.1f} hours old). Fetching new data...")
    else:
        print("[CACHE] Force fetch or feed missing. Fetching from API...")

    # 2. Fetch from API
    try:
        response = requests.get(
            URL, 
            auth=HTTPBasicAuth(API_KEY, API_SECRET),
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        # 3. Validation
        if not data.get("result"):
            print(f"[ERROR] API returned result=False: {data.get('message')}")
            return None

        # 4. Save to Disk
        with open(FEED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[SUCCESS] Saved {len(data.get('products', []))} products to {FEED_FILE}")
        return data

    except Exception as e:
        print(f"[ERROR] Failed to fetch Maya plans: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Maya Mobile Plans")
    parser.add_argument("--force", action="store_true", help="Ignore cache and force fetch")
    args = parser.parse_args()
    
    fetch_maya_plans(force=args.force)
